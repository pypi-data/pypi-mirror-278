# coding: utf-8

class AlicloudOSS:
  def __init__(self, access, secret, bucket, region='ap-southeast-1', endpoint=''):
    from oss2 import Auth, Bucket
    if not endpoint: endpoint = f'https://oss-{region}.aliyuncs.com'
    self.login = Bucket(
      auth = Auth(access, secret),
      endpoint = endpoint,
      bucket_name = bucket,
    )
    self.bucket = bucket


  def list_object(self, prefix=''):
    from oss2 import ObjectIteratorV2
    from pandas import DataFrame
    from oahspe.tool import parse_key
    from datetime import datetime
    content = []
    for obj in ObjectIteratorV2(self.login, prefix):
      key, prefix = parse_key(obj.key)
      content.append({
        'key': key,
        'prefix': prefix,
        'modified': datetime.fromtimestamp(int(obj.last_modified)),
        'etag': obj.etag.lower(),
        'size': int(obj.size),
      })
    content = DataFrame(content)
    return content


  def head_object(self, key):
    from datetime import datetime
    obj = self.login.head_object(key)
    return {
      'modified': datetime.fromtimestamp(int(obj.last_modified)),
      'size': int(obj.content_length),
      'type': obj.content_type,
      'etag': obj.etag.lower(),
    }
  

  def get_object(self, key) -> bytes:
    with self.login.get_object(key) as f:
      res = f.read()
    return res


  def put_object(self, key, data):
    if not isinstance(data, str|bytes): data = str(data)
    self.login.put_object(key=key, data=data)
  

  def delete_object(self, key):
    self.login.delete_object(key)


  def put_file(self, local, key):
    self.login.put_object_from_file(key, local)


  def copy_object(self, src_key, dst_key, src_bucket=None):
    if src_bucket is None: src_bucket = self.bucket
    self.login.copy_object(source_bucket_name=self.bucket, source_key=src_key, target_key=dst_key)


  def move_object(self, src_key, dst_key, src_bucket=None):
    self.copy_object(src_key, dst_key, src_bucket)
    if src_bucket is None:
      self.delete_object(src_key)


  def delete_prefix(self, prefix=''):
    danhsach = self.list_object(prefix)
    if len(danhsach) == 0: return
    danhsach = danhsach['key'].to_list()
    if prefix:
      danhsach = [prefix + '/' + key for key in danhsach]
    for key in danhsach:
      self.delete_object(key)
  

  def create_bucket(self):
    return self.login.create_bucket()
  

  def delete_bucket(self):
    self.delete_prefix()
    self.login.delete_bucket()
  
