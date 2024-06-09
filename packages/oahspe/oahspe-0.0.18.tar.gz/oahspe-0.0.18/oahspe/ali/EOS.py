# coding: utf-8

import pandas as pd
from oahspe.tool import *
from datetime import datetime
from threading import Thread

class AlicloudEOS:
  def __init__(self, access, secret, bucket):
    from oss2 import Auth, Bucket
    self.access = access
    self.secret = secret
    self.endpoint = 'https://eos.aliyuncs.com'
    self.login = Bucket(
      auth = Auth(access, secret),
      endpoint = self.endpoint,
      bucket_name = bucket,
    )
    self.bucket = bucket
    self.ossutil = f'ossutil64 -i {access} -k {secret} -e {self.endpoint}'
  
  def cli(self, code):
    return bash_out(f'{self.ossutil} {code}')
  
  def list_object(self, prefix='', delimiter=''):
    content = []
    for obj in self.list_object_(prefix, delimiter):
      key, prefix = parse_key(obj.key)
      content.append({
        'key': key,
        'prefix': prefix,
        'modified': datetime.fromtimestamp(int(obj.last_modified)),
        'etag': obj.etag.lower(),
        'size': int(obj.size),
      })
    content = pd.DataFrame(content)
    return content

  def list_object_(self, prefix='', delimiter=''):
    from oss2 import ObjectIterator
    return ObjectIterator(self.login, prefix, delimiter)
  
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
    bash(f'''
chmod 600 {conf}
s3fs {self.bucket} {mnt} \
  -o passwd_file={conf} \
  -o url={self.endpoint} \
  {option}
sleep 2
''')
    return conf, mnt

  def dir_ls(self, depth=1):
    conf, mnt = self.mount()
    try:
      folders, files = dir_ls(mnt, depth)
    finally:
      bash(f'''
  umount {mnt} 2> /dev/null
  sleep 0.5
  rm -rf {conf}
  rm -rf {mnt}
  ''')
    return folders, files

  def dir_detail_prefix(self, prefix):
    size = [int(obj.size) for obj in self.list_object_(prefix+'/')]
    if not size: return {}
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
    try:
      obj = self.login.head_object(obj)
      return {
        'type': 'object',
        'size': int(obj.content_length),
        'count': 1,
        'last': now(),
      }
    except: return {}

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
    res = pd.DataFrame.from_dict(res, orient='index')
    res.index.names = ['key']
    return res
