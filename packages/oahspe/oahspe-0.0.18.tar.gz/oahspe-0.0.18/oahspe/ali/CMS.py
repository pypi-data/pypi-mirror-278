# coding: utf-8

from alibabacloud_cms20190101.models import *
from time import sleep
from random import random


class AlicloudCMS:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_cms20190101.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'metrics.{region}.aliyuncs.com'
    ))
    self.region_id = region

  @property
  def login(self):
    sleep(3*random())
    return self._login
