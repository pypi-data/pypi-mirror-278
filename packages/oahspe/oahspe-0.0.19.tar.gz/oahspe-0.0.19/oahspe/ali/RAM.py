# coding: utf-8

from alibabacloud_ram20150501.models import *
from time import sleep
from random import random
from oahspe.tool import setdefault


class AlicloudRAM:
  def __init__(self, access, secret):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_ram20150501.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = 'ram.aliyuncs.com',
    ))

  @property
  def login(self):
    sleep(3*random())
    return self._login
  

  def create_user(self, args):
    print('[RAM Create User]')
    args = setdefault(args, ['display_name', args['user_name']])
    print(args)
    user_name = args['user_name']
    res = self.login.create_user(CreateUserRequest(**args))
    user_id = res.body.user.user_id
    res = self.login.create_access_key(CreateAccessKeyRequest(user_name=user_name))
    access_key_id = res.body.access_key.access_key_id
    access_key_secret = res.body.access_key.access_key_secret
    return user_id, access_key_id, access_key_secret


  def create_policy(self, args):
    print('[RAM][Create Policy]')
    print(args)
    res = self.login.create_policy(CreatePolicyRequest(**args))
    policy_type = res.body.policy.policy_type
    return policy_type


  def attach_policy_to_user(self, args):
    print('[RAM][Attach Policy]')
    print(args)
    self.login.attach_policy_to_user(AttachPolicyToUserRequest(**args))


  def delete_user(self, args):
    print('[RAM][Delete User]')
    print(args)
    self.login.delete_access_key(DeleteAccessKeyRequest(**args))
    self.login.delete_user(DeleteUserRequest(args['user_name']))


  def delete_policy(self, policy_name):
    print('[RAM Delete Policy]')
    print(policy_name)
    self.login.delete_policy(DeletePolicyRequest(policy_name))


  def detach_policy_from_user(self, args):
    print('[RAM Detach Policy From User]')
    print(args)
    self.login.detach_policy_from_user(DetachPolicyFromUserRequest(**args))
