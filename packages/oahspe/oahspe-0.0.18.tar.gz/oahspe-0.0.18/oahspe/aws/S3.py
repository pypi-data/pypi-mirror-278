# coding: utf-8

from oahspe.tool import *
from pandas import DataFrame
from threading import Thread

class AwsS3:
  def __init__(self, access, secret, endpoint, bucket=None):
    from boto3 import client
    self.access = access
    self.secret = secret
    self.endpoint = endpoint
    self.login = client(
      's3',
      aws_access_key_id = access,
      aws_secret_access_key = secret,
      endpoint_url = endpoint
    )
    self.bucket = bucket
    self.awscli = f'AWS_ACCESS_KEY_ID={access} AWS_SECRET_ACCESS_KEY={secret} aws --endpoint-url {endpoint}'


  def list_object(self, prefix='', delimiter=''):
    content = []
    for obj in self.list_object_(prefix, delimiter):
      key, prefix = parse_key(obj['Key'])
      content.append({
        'key': key,
        'prefix': prefix,
        'size': int(obj['Size']),
        'etag': obj['ETag'].strip('"'),
        'modified': obj['LastModified'],
      })
    content = DataFrame(content)
    return content
  

  def list_object_(self, prefix='', delimiter=''):
    content = []
    for page in self.login.get_paginator('list_objects_v2').paginate(Bucket=self.bucket, Prefix=prefix, Delimiter=delimiter):
      if 'Contents' in page:
        content.extend(page['Contents'])
    return content


  def transfer_config(self, args={}):
    from boto3.s3.transfer import TransferConfig
    args = setdefault(args, {
      'multipart_threshold': 100*1024*1024+1,
      'multipart_chunksize': 100*1024*1024,
      'use_threads': True,
      'max_concurrency': 16,
    })
    self.transfer = TransferConfig(**args)
  

  def copy_object(self, src_key, dst_key, dst_bucket=None):
    if dst_bucket is None: dst_bucket = self.bucket
    self.login.copy_object(Bucket=self.bucket, CopySource={'Bucket':dst_bucket,'Key':src_key}, Key=dst_key)


  def delete_object(self, key):
    self.login.delete_object(Bucket=self.bucket, Key=key)


  def move_object(self, src_key, dst_key, dst_bucket=None):
    self.copy_object(src_key, dst_key, dst_bucket)
    self.delete_object(src_key)


  def put_object(self, key, data):
    self.login.put_object(Bucket=self.bucket, Key=key, Body=data)


  def put_local(self, local, key, type='bz2', checksum=False):
    if isinstance(local, str):
      if os.path.isfile(local): return self.put_file(local, key, checksum)
      elif os.path.isdir(local): return self.put_folder(local, key, type, checksum)
    local = tmp_write(to_byte(local))
    res = self.put_file(local, key, checksum)
    os.remove(local)
    return res


  def put_file(self, local, key, checksum=False):
    if not hasattr(self, 'transfer'): self.transfer_config()
    self.login.upload_file(local, Bucket=self.bucket, Key=key, Config=self.transfer)
    if checksum:
      return self.checksum(local, key)


  def put_folder(self, local, key, type='bz2', checksum=False):
    local = tar(local, type=type)
    res = self.put_file(local, key, checksum)
    os.remove(local)
    return res


  def checksum(self, local, key):
    from math import floor
    head = self.head_object(key)
    size, etag = head['size'], head['etag']
    chunk = floor(size / int(etag.split('-')[-1])) if '-' in etag else size
    return checksum(local, chunk) == etag


  def head_object(self, key):
    res = self.login.head_object(Bucket=self.bucket, Key=key)
    return {
      'modified': res['LastModified'],
      'size': int(res['ContentLength']),
      'etag': res['ETag'].strip('"'),
      'type': res['ContentType'],
    }

  def get_object(self, key) -> bytes:
    with self.login.get_object(Bucket=self.bucket, Key=key)['Body'] as f:
      res = f.read()
    return res
  

  def delete_prefix(self, prefix='', delimiter=''):
    danhsach = self.list_object(prefix, delimiter)
    if len(danhsach) == 0: return
    danhsach = danhsach['key'].to_list()
    if prefix:
      danhsach = [prefix + '/' + key for key in danhsach]
    for key in danhsach:
      self.delete_object(key)


  def list_bucket(self):
    return DataFrame([{
      'name': obj['Name'],
      'creation_date': obj['CreationDate'],
    } for obj in self.login.list_buckets()['Buckets']])


  def create_bucket(self):
    self.login.create_bucket(Bucket=self.bucket)
  

  def delete_bucket(self):
    self.delete_prefix()
    self.login.delete_bucket(Bucket=self.bucket)


  def mount(self):
    conf = '/tmp/' + gen_uuid()
    mnt = '/tmp/' + gen_uuid()
    bash(f'''
umount {mnt} 2> /dev/null
sleep 0.5
rm -rf {conf}
rm -rf {mnt}
mkdir -p {mnt}
''')
    with open(conf, 'w') as f: f.write(self.access + ':' + self.secret)
    option = '-o rw -o _netdev -o allow_other'
    if 'cloudstorage.com.vn' in self.endpoint: option += ' -o use_path_request_style'
    bash(f'''
chmod 600 {conf}
s3fs {self.bucket} {mnt} \
  -o passwd_file={conf} \
  -o url={self.endpoint} \
  {option}
sleep 2
''')
    return conf, mnt

  def umount(conf, mnt):
    bash(f'''
  umount {mnt} 2> /dev/null
  sleep 0.5
  rm -rf {conf}
  rm -rf {mnt}
  ''')


  def dir_detail_prefix(self, prefix):
    size = [int(obj['Size']) for obj in self.list_object_(prefix+'/')]
    size_sum = sum(size)
    size_count = len(size)
    size_mean = size_sum/size_count
    return {
      'type': 'prefix',
      'size': size_sum,
      'count': size_count,
      'last': now(),
      'mean': size_mean,
    }

  def dir_detail_object(self, obj):
    return {
      'type': 'object',
      'size': int(self.login.head_object(Bucket=self.bucket, Key=obj)['ContentLength']),
      'count': 1,
      'last': now(),
    }

  def dir_detail(self, folders, files):
    res = {}
    def func(fold):
      tmp = self.dir_detail_prefix(fold)
      if tmp: res[fold] = tmp
    folders = [Thread(target=func, args=[fold]) for fold in folders]
    for fold in folders:
      fold.start()
    for file in files:
      res[file] = self.dir_detail_object(file)
    for fold in folders:
      fold.join()
    res = DataFrame.from_dict(res, orient='index')
    res.index.names = ['key']
    return res

  def cli(self, code):
    return bash_out(f'{self.awscli} {code}')

  def dir1(self, prefix=''):
    if prefix: prefix += '/'
    folders, files = [], []
    for row in self.cli(f's3 ls s3://{self.bucket}/{prefix}').splitlines():
      row = row.strip()
      if 'PRE' in row:
        row = row.split(' ')[-1][:-1]
        folders.append(row)
      else:
        row = row.split(' ')[-1]
        files.append(row)
    return folders, files
  
  def dir_(self, func):
    folders1, files = func()
    folders = []
    for fold1 in folders1:
      folders2, files2 = self.dir1(fold1)
      files.extend([f'{fold1}/{file2}' for file2 in files2])
      folders.extend([f'{fold1}/{fold2}' for fold2 in folders2])
    return folders, files

  def dir2(self): return self.dir_(self.dir1)
  def dir3(self): return self.dir_(self.dir2)
  def dir4(self): return self.dir_(self.dir3)
  def dir5(self): return self.dir_(self.dir4)
  def dir6(self): return self.dir_(self.dir5)
  def dir7(self): return self.dir_(self.dir6)

  def dir(self, depth=1):
    return {
      1: self.dir1,
      2: self.dir2,
      3: self.dir3,
      4: self.dir4,
      5: self.dir5,
      6: self.dir6,
      7: self.dir7,
    }[depth]()