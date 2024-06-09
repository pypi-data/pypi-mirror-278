# coding: utf-8

from alibabacloud_ecs20140526.models import *
from base64 import b64encode
from os.path import exists
from time import sleep
from copy import copy
from random import random
from oahspe.tool import setdefault


class AlicloudECS:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_ecs20140526.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'ecs.{region}.aliyuncs.com',
    ))
    self.region_id = region

  @property
  def login(self):
    sleep(3*random())
    return self._login


# --------------------------------------------------------------------------------
# INSTANCES
# --------------------------------------------------------------------------------
  def describe_instances(self, instance_id):
    return self.login.describe_instances(DescribeInstancesRequest(
      region_id = self.region_id,
      instance_ids = [instance_id],
    )).body.instances.instance


  def start_instance(self, instance_id):
    print('[ECS][Instance][Start]')
    print(instance_id)
    self.login.start_instance(StartInstanceRequest(instance_id=instance_id))
    check = lambda: self.describe_instances(instance_id)[0]
    res = check()
    while res.status != 'Running':
      print('[ECS][Instance][Start] Working...')
      sleep(2)
      res = check()
    print('[ECS][Instance][Start] Done')


  def reboot_instance(self, instance_id):
    print('[ECS][Instance][Reboot]')
    print(instance_id)
    self.login.reboot_instance(RebootInstanceRequest(instance_id=instance_id))
    check = lambda: self.describe_instances(instance_id)[0]
    res = check()
    while res.status != 'Running':
      print('[ECS][Instance][Start] Working...')
      sleep(2)
      res = check()
    print('[ECS][Instance][Start] Done')
  

  def create_instance(self, name, args):
    print('[ECS][Instance][Create]')
    disk_name_system = f'sys-{name}'
    args = setdefault(args, {
      'instance_name', name,
      'host_name', name,
      'instance_name', name,
      'region_id', self.region_id,
    })
    args['system_disk'] = setdefault(args['system_disk'], ['disk_name', disk_name_system])
    print(args)
    args['system_disk'] = CreateInstanceRequestSystemDisk(**args['system_disk'])
    disk_name_data = []
    if 'data_disk' in args:
      disk_name_data =  [d['disk_name'] for d in args['data_disk']]
      args['data_disk'] = [CreateInstanceRequestDataDisk(**d) for d in args['data_disk']]
    res = self.login.create_instance(CreateInstanceRequest(**args))
    instance_id = res.body.instance_id
    sleep(5)
    res = self.start_instance(instance_id)
    primary_ip_address = res.network_interfaces.network_interface[0].primary_ip_address
    return instance_id, disk_name_system, disk_name_data, primary_ip_address


  def delete_instance(self, instance_id):
    print('[ECS][Instance][Delete]')
    print(instance_id)
    self.login.delete_instance(DeleteInstanceRequest(
      instance_id = instance_id,
      force = True,
    ))
    while len(self.describe_instances(instance_id)[0]):
      sleep(2)
      print('[ECS][Instance][Delete] Working')
    print('[ECS][Instance][Delete] Done')


# --------------------------------------------------------------------------------
# SECURITY GROUP
# --------------------------------------------------------------------------------   
  def describe_security_group(self, security_group_id):
    return self.login.describe_security_group(DescribeSecurityGroupsRequest(
      region_id = self.region_id,
      security_group_id = security_group_id,
    )).body.security_groups.security_group


  def create_security_group(self, args):
    print('[ECS][Security Group][Create]')
    args = setdefault(args, {
      'region_id', self.region_id,
      'security_group_type', 'enterprise',
    })
    print(args)
    res = self.login.create_security_group(CreateSecurityGroupRequest(**args))
    security_group_id = res.body.security_group_id
    return security_group_id


  def authorize_security_group(self, args):
    print('[ECS][Security Group][Authorize]')
    args = setdefault(args, {
      'region_id', self.region_id,
      'policy', 'accept',
    })

    print(args)
    self.login.authorize_security_group(AuthorizeSecurityGroupRequest(**args))


  def authorize_security_group_egress(self, args):
    print('[ECS][Security Group][Authorize Egress]')
    args = setdefault(args, {
      'region_id', self.region_id,
      'policy', 'accept',
    })
    print(args)
    self.login.authorize_security_group_egress(AuthorizeSecurityGroupEgressRequest(**args))
 

  def delete_security_group(self, security_group_id):
    print('[ECS][Security Group][Delete]')
    print(security_group_id)
    self.login.delete_security_group(DeleteSecurityGroupRequest(
      region_id = self.region_id,
      security_group_id = security_group_id,
    ))
    while len(self.describe_security_group(security_group_id)):
      print('[ECS][Security Group][Delete] Working...')
      sleep(2)
    print('[ECS][Security Group][Delete] Done')


# --------------------------------------------------------------------------------
# CLOUD ASSSITANT
# --------------------------------------------------------------------------------
  def install_cloud_assistant(self, instance_id):
    print('[ECS][Cloud Assistant][Install]')
    print(instance_id)
    self.login.install_cloud_assistant(InstallCloudAssistantRequest(
      instance_id = [instance_id],
      region_id = self.region_id
    ))


  def send_file(self, args):
    print('[ECS][Cloud Assistant][Send File]')
    args = setdefault(args, {
      'region_id', self.region_id,
    })
    cmd = args['content']
    if exists(cmd):
      with open(cmd, 'w') as f:
        cmd = f.read()
    args['content'] = b64encode(cmd.encode('UTF-8'))
    args_print = copy(args)
    del args_print['content']
    print(args_print)
    self.login.send_file(SendFileRequest(**args))


  def describe_invocations(self, invoke_id):
    return self.login.describe_invocations(DescribeInvocationsRequest(
      invoke_id = invoke_id,
      region_id = self.region_id,
    )).body.invocations.invocation


  def invoke_command(self, instance_id, args):
    print('[ECS][Cloud Assistant][Invoke Command]')
    args = setdefault(args, ['region_id', self.region_id])
    cmd = args['command_content']
    if exists(cmd):
      with open(cmd, 'w') as f:
        cmd = f.read()
    args['command_content'] = b64encode(cmd.encode('UTF-8'))
    args_print = copy(args)
    del args_print['command_content']
    print(args_print)
    res = self.login.create_command(CreateCommandRequest(**args))
    command_id = res.body.command_id

    res = self.login.invoke_command(InvokeCommandRequest(
      command_id = command_id,
      instance_id = [instance_id],
      region_id = self.region_id,
      timeout = args['timeout'],
    ))
    invoke_id = res.body.invoke_id

    check = lambda: self.describe_invocations(invoke_id)[0]
    res = check()
    while res.invoke_status != 'Finished':
      if res.invoke_status == 'Stopped':
        raise RuntimeError()
      print('[ECS][Cloud Assistant][Invoke Command] Working...')
      sleep(10)
      res = check()
    print('[ECS][Cloud Assistant][Invoke Command] Done')

    self.login.delete_command(DeleteCommandRequest(
      command_id = command_id,
      region_id = self.region_id,
    ))


# --------------------------------------------------------------------------------
# SNAPSHOT
# --------------------------------------------------------------------------------
  def describe_snapshots(self, snapshot_id):
    return self.login.describe_snapshots(DescribeSnapshotsRequest(
      snapshot_ids = str([snapshot_id]),
      region_id = self.region_id,
    )).body.snapshots.snapshot

  def create_snapshot(self, args):
    print('[ECS][Snapshot][Create]')
    print(args)
    res = self.login.create_snapshot(CreateSnapshotRequest(**args))
    snapshot_id = res.body.snapshot_id
    check = lambda: self.describe_snapshots(snapshot_id)[0]
    res = check()
    while not res.available:
      print(f'[ECS][Snapshot][Create] Working... {res.progress}')
      sleep(5)
      res = check()
    print('[ECS][Snapshot][Create] Done')
    return snapshot_id

  def delete_snapshot(self, snapshot_id):
    print('[ECS][Snapshot][Delete]')
    print(snapshot_id)
    self.login.delete_snapshot(DeleteSnapshotRequest(
      snapshot_id = snapshot_id,
      force = True,
    ))
    while len(self.describe_snapshots(snapshot_id)):
      print('[ECS][Snapshot][Delete] Working...')
      sleep(2)
    print('[ECS][Snapshot][Delete] Done')


# --------------------------------------------------------------------------------
# IMAGE
# --------------------------------------------------------------------------------
  def describe_images(self, image_id):
    return self.login.describe_images(DescribeImagesRequest(
      image_id = image_id,
      region_id = self.region_id,
    )).body.images.image


  def create_image(self, args):
    print('[ECS][Image][Create]')
    args = setdefault(args, ['region_id', self.region_id])
    print(args)
    res = self.login.create_image(CreateImageRequest(**args))
    image_id = res.body.image_id
    sleep(60)

    check = lambda: self.describe_images(image_id)[0]
    res = check()
    snapshot_id_base = res.disk_device_mappings.disk_device_mapping[0].snapshot_id

    while res.status != 'Available':
      print(f'[ECS][Image][Create] Working... {res.progress}')
      sleep(2)
      res = check()
    print('[ECS][Image][Create] Done')
    return image_id, snapshot_id_base


  def delete_image(self, image_id):
    print('[ECS][Image][Delete]')
    print(image_id)
    self.login.delete_image(DeleteImageRequest(
      force = True,
      image_id = image_id,
      region_id = self.region_id,
    ))
    while len(self.describe_images(image_id)):
      print('[ECS][Image][Delete] Working...')
      sleep(2)
    print('[ECS][Image][Delete] Done')
