# coding: utf-8

from alibabacloud_sas20181203.models import *
from time import sleep
from random import random


class AlicloudSAS:
  def __init__(self, access, secret):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_sas20181203.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = 'tds.aliyuncs.com',
    ))

  @property
  def login(self):
    sleep(3*random())
    return self._login
