# coding: utf-8

from alibabacloud_kms20160120.models import *
from time import sleep
from random import random
from oahspe.tool import setdefault


class AlicloudKMS:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_kms20160120.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'kms.{region}.aliyuncs.com',
    ))
    self.region_id = region

  @property
  def login(self):
    sleep(3*random())
    return self._login
  


  def list_keys(self):
    res = self.login.list_keys(ListKeysRequest())
    ls_key = res.body.keys.key
    return ls_key
  
  def encrypt(self, key_id, plaintext):
    res = self.login.encrypt(EncryptRequest(
      key_id = key_id,
      plaintext = plaintext,
    ))
    ciphertext_blob = res.body.ciphertext_blob
    return ciphertext_blob
  
  def decrypt(self, ciphertext_blob):
    res = self.login.decrypt(DecryptRequest(ciphertext_blob=ciphertext_blob))
    plaintext = res.body.plaintext
    return plaintext

  def generate_data_key(self, args):
    args = setdefault(args, ['key_spec', 'AES_256'])
    res = self.login.generate_data_key(GenerateDataKeyRequest(**args))
    ciphertext_blob = res.body.ciphertext_blob
    plaintext = res.body.plaintext
    return ciphertext_blob, plaintext


