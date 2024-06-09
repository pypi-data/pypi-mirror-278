# coding: utf-8

from alibabacloud_cas20200407.models import *
from time import sleep
from random import random


class AlicloudCAS:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_cas20200407.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'cas.{region}.aliyuncs.com'
    ))
    self.id_region = region

  @property
  def login(self):
    sleep(3*random())
    return self._login


# --------------------------------------------------------------------------------
# UPLOAD CERTIFICATE
# --------------------------------------------------------------------------------
  def upload_cert(self, args):
    print('[CAS][Upload User Certificate]')
    print(args)
    res = self.login.upload_user_certificate(UploadUserCertificateRequest(**args))
    cert_id = res.body.cert_id
    return cert_id


  def delete_cert(self, cert_id):
    print('[CAS][Delete User Certificate]')
    print(cert_id)
    self.login.delete_user_certificate(DeleteUserCertificateRequest(cert_id))


  def get_cert(self, cert_id):
    from datetime import datetime
    print('[CAS][Get User Certificate]')
    print(cert_id)
    res = self.login.get_user_certificate_detail(GetUserCertificateDetailRequest(cert_id=cert_id))
    res = res.body
    y,m,d = res.start_date.split('-')
    start_date = datetime(year=int(y),month=int(m),day=int(d))
    y,m,d = res.end_date.split('-')
    end_date = datetime(year=int(y),month=int(m),day=int(d))
    return res.cert, res.key, res.sans, start_date, end_date
