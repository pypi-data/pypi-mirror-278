# coding: utf-8

from alibabacloud_vpc20160428.models import *
from time import sleep
from random import random
from oahspe.tool import setdefault


class AlicloudVPC:
  def __init__(self, access, secret, region):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_vpc20160428.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = f'vpc.{region}.aliyuncs.com',
    ))
    self.region_id = region

  @property
  def login(self):
    sleep(3*random())
    return self._login


# --------------------------------------------------------------------------------
# VPC
# --------------------------------------------------------------------------------
  def describe_vpcs(self, vpc_id):
    return self.login.describe_vpcs(DescribeVpcsRequest(
      vpc_id = vpc_id,
      region_id = self.region_id,
    )).body.vpcs.vpc


  def create_vpc(self, args):
    print('[VPC][VPC][Create]')
    args = setdefault(args, ['region_id', self.region_id])
    print(args)
    res = self.login.create_vpc(CreateVpcRequest(**args))
    res = res.body
    vpc_id = res.vpc_id
    route_table_id = res.route_table_id
    vrouter_id = res.vrouter_id
 
    check = lambda: self.describe_vpcs(vpc_id)[0]
    res = check()
    while res.status != 'Available':
      print('[VPC][VPC][Create] Working...')
      sleep(2)
      res = check()
    print('[VPC][VPC][Create] Done')
    return vpc_id, route_table_id, vrouter_id


  def delete_vpc(self, vpc_id):
    print('[VPC][VPC][Delete]')
    print(vpc_id)
    self.login.delete_vpc(DeleteVpcRequest(
      vpc_id = vpc_id,
      force_delete = True,
      region_id = self.region_id,
    ))
    while len(self.describe_vpcs(vpc_id)):
      print('[VPC][VPC][Delete] Working...')
      sleep(2)
    print('[VPC][VPC][Delete] Done')


# --------------------------------------------------------------------------------
# VSWITCH
# --------------------------------------------------------------------------------
  def describe_vswitches(self, v_switch_id):
    return self.login.describe_vswitches(DescribeVSwitchesRequest(
      v_switch_id = v_switch_id,
      region_id = self.region_id,
    )).body.v_switches.v_switch


  def create_vswitch(self, args):
    print('[VPC][vSwitch][Create]')
    args = setdefault(args, ['region_id', self.region_id])
    print(args)
    res = self.login.create_vswitch(CreateVSwitchRequest(**args))
    v_switch_id = res.body.v_switch_id
    check = lambda: self.describe_vswitches(v_switch_id)[0]
    res = check()
    while res.status != 'Available':
      print('[VPC][vSwitch][Create] Working...')
      sleep(2)
      res = check()
    print('[VPC][vSwitch][Create] Done')
    return v_switch_id


  def delete_vswitch(self, v_switch_id):
    print('[VPC][vSwitch][Delete]')
    print(v_switch_id)
    self.login.delete_vswitch(DeleteVSwitchRequest(
      v_switch_id = v_switch_id,
      region_id = self.region_id,
    ))
    while len(self.describe_vswitches(v_switch_id)):
      print('[VPC][vSwitch][Delete] Working...')
      sleep(2)
    print('[VPC][vSwitch][Delete] Done')


# --------------------------------------------------------------------------------
# EIP
# --------------------------------------------------------------------------------
  def describe_eip_addresses(self, allocation_id):
    return self.login.describe_eip_addresses(DescribeEipAddressesRequest(
      allocation_id = allocation_id,
      region_id = self.region_id,
    )).body.eip_addresses.eip_address
  

  def allocate_eip_address(self, args):
    print('[VPC][EIP][Allocate]')
    args = setdefault(args, ['region_id', self.region_id])
    print(args)
    res = self.login.allocate_eip_address(AllocateEipAddressRequest(**args))
    eip_address = res.body.eip_address
    allocation_id = res.body.allocation_id
    check = lambda: self.describe_eip_addresses(allocation_id)[0]
    res = check()
    while res.status != 'Available':
      print('[VPC][EIP][Allocate] Working...')
      sleep(2)
      res = check()
    print('[VPC][EIP][Allocate] Done')
    return eip_address, allocation_id


  def release_eip_address(self, allocation_id):
    print('[VPC][EIP][Release]')
    print(allocation_id)
    self.login.release_eip_address(ReleaseEipAddressRequest(
      allocation_id = allocation_id,
      region_id = self.region_id,
    ))
    while len(self.describe_eip_addresses(allocation_id)):
      print('[VPC][EIP][Release] Working...')
      sleep(2)
    print('[VPC][EIP][Release] Done')


  def associate_eip_address(self, args):
    print('[VPC][EIP][Associate]')
    args = setdefault(args, ['region_id', self.region_id])
    print(args)
    self.login.associate_eip_address(AssociateEipAddressRequest(**args))
    check = lambda: self.describe_eip_addresses(args['allocation_id'])[0]
    res = check()
    while res.status != 'InUse':
      print('[VPC][EIP][Associate] Working...')
      sleep(2)
      res = check()
    print('[VPC][EIP][Associate] Done')


# --------------------------------------------------------------------------------
# ROUTE TABLE
# --------------------------------------------------------------------------------
  def create_route_entry(self, args):
    print('[VPC][Route Table][Create Route Entry]')
    args = setdefault(args, 'region_id', self.region_id)
    print(args)
    res = self.login.create_route_entry(CreateRouteEntryRequest(**args))
    route_entry_id = res.body.route_entry_id
    return route_entry_id


  def delete_route_entry(self, route_entry_id):
    print('[VPC][Route Table][Delete Route Entry]')
    print(route_entry_id)
    self.login.delete_route_entry(DeleteRouteEntryRequest(
      route_entry_id = route_entry_id,
      region_id = self.region_id,
    ))
