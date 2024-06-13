# coding: utf-8

from alibabacloud_ess20220222.models import *
from time import sleep
from random import random

class AlicloudESS:
  def __init__(self, access, secret):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_ess20220222.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = 'ess.aliyuncs.com',
    ))


  @property
  def login(self):
    sleep(3*random())
    return self._login
