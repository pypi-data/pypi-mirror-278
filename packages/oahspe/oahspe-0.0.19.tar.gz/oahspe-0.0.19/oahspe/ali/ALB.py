# coding: utf-8


from alibabacloud_alb20200616.models import *
from random import random
from time import sleep


class AlicloudALB:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_alb20200616.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'alb.{region}.aliyuncs.com'
    ))
    self.region_id = region

  @property
  def login(self):
    sleep(3*random())
    return self._login


# --------------------------------------------------------------------------------
# SERVER GROUP
# --------------------------------------------------------------------------------
  def create_server_group(self, args):
    print('[ALB][Server Group][Create]')
    print(args)
    args['health_check_config'] = CreateServerGroupRequestHealthCheckConfig(**args['health_check_config'])
    args['sticky_session_config'] = CreateServerGroupRequestStickySessionConfig(**args['sticky_session_config'])
    args = CreateServerGroupRequest(**args)
    res = self.login.create_server_group(args)
    server_group_id = res.body.server_group_id
    job_id = res.body.job_id
    return server_group_id, job_id


  def delete_server_group(self, server_group_id):
    print('[ALB][Server Group][Delete]')
    print(server_group_id)
    self.login.delete_server_group(DeleteServerGroupRequest(server_group_id))
