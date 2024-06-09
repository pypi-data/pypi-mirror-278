# coding: utf-8

from alibabacloud_nas20170626.models import *
from time import sleep
from random import random
from oahspe.tool import setdefault


class AlicloudNAS:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_nas20170626.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'nas.{region}.aliyuncs.com',
    ))
    self.region_id = region

  @property
  def login(self):
    sleep(3*random())
    return self._login
  

# --------------------------------------------------------------------------------
# FILE SYSTEM
# --------------------------------------------------------------------------------
  def describe_file_systems(self, file_system_id):
    return self.login.describe_file_systems(DescribeFileSystemsRequest(
      file_system_id = file_system_id,
    )).body.file_systems.file_system


  def create_file_system(self, args):
    print('[NAS][File System][Create]')
    args = setdefault(args, {
      'charge_type', 'PayAsYouGo',
      'protocol_type', 'NFS',
      'encrypt_type', 0,
    })
    print(args)
    res = self.login.create_file_system(CreateFileSystemRequest(**args))
    file_system_id = res.body.file_system_id
    print(file_system_id)

    check = lambda: self.describe_file_systems(file_system_id)[0]
    res = check()
    while res.status != 'Running':
      print('[NAS][File System][Create] Working...')
      sleep(2)
      res = check()
    print('[NAS][File System][Create] Done')
    return file_system_id


  def delete_file_system(self, file_system_id):
    print('[NAS][File System][Delete]')
    print(file_system_id)
    self.login.delete_file_system(DeleteFileSystemRequest(file_system_id=file_system_id))
    while len(self.describe_file_systems(file_system_id)):
      print('[NAS][File System][Delete] Working...')
      sleep(2)
    print('[NAS][File System][Delete] Done')


# --------------------------------------------------------------------------------
# ACCESS GROUP
# --------------------------------------------------------------------------------
  def create_access_group(self, args):
    print('[NAS][Access Group][Create]')
    print(args)
    req = CreateAccessGroupRequest(**args)
    self.login.create_access_group(req)


  def delete_access_group(self, access_group_name):
    print('[NAS][Access Group][Delete]')
    print(access_group_name)
    self.login.delete_access_group(DeleteAccessGroupRequest(access_group_name=access_group_name))


  def create_access_rule(self, args):
    print('[NAS][Access Group][Access Rule Create]')
    print(args)
    self.login.create_access_rule(CreateAccessRuleRequest(**args))


# --------------------------------------------------------------------------------
# MOUNT TARGET
# --------------------------------------------------------------------------------
  def describe_mount_targets(self, mount_target_domain):
    return self.login.describe_mount_targets(DescribeFileSystemsRequest(
      mount_target_domain=mount_target_domain
    )).body.mount_targets.mount_target


  def create_mount_target(self, args):
    print('[NAS][Mount Target][Create]')
    print(args)
    res = self.login.create_mount_target(CreateMountTargetRequest(**args))
    mount_target_domain = res.body.mount_target_domain
    check = lambda: self.describe_mount_targets(mount_target_domain)[0]
    res = check()
    while res.status != 'Active':
      print('[NAS][Mount Target][Create] Working...')
      sleep(5)
      res = check()
    print('[NAS][Mount Target][Create] Done')
    return mount_target_domain


  def delete_mount_target(self, mount_target_domain):
    print('[NAS][Mount Target][Delete]')
    print(mount_target_domain)
    self.login.delete_mount_target(DeleteMountTargetRequest(mount_target_domain=mount_target_domain))
    while len(self.describe_mount_targets(mount_target_domain)):
      print('[NAS][Mount Target][Delete] Working...')
      sleep(2)
    print('[NAS][Mount Target][Delete] Done')
