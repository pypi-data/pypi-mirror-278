# coding: utf-8

from alibabacloud_cdn20180510.models import *
from oahspe.clf.DNS import CloudflareDNS
from random import random
from oahspe.tool import setdefault
from time import sleep


class AlicloudCDN:
  def __init__(self, access, secret):
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_cdn20180510.client import Client
    self._login = Client(Config(
      access_key_id = access,
      access_key_secret = secret,
      endpoint = 'cdn.aliyuncs.com'
    ))

  @property
  def login(self):
    sleep(3*random())
    return self._login


# --------------------------------------------------------------------------------
# CDN DOMAIN
# --------------------------------------------------------------------------------
  def add_cdn_domain(self, args):
    print('[CDN][CDN Domain][Add]')
    args = setdefault(args, ['scope', 'overseas'])
    print(args)
    self.login.add_cdn_domain(AddCdnDomainRequest(**args))


  def delete_cdn_domain(self, domain_name):
    print('[CDN][CDN Domain][Delete]')
    print(domain_name)
    self.login.delete_cdn_domain(DeleteCdnDomainRequest(domain_name=domain_name))


  def verify_domain_owner(self, domain_name):
    print('[CDN][CDN Domain][Verify]')
    print(domain_name)
    res = self.login.verify_domain_owner(VerifyDomainOwnerRequest(domain_name=domain_name))
    content = res.body.content
    return content


# --------------------------------------------------------------------------------
# CERTIFICATE
# --------------------------------------------------------------------------------
  def set_cdn_domain_sslcertificate(self, args):
    print('[[CDN][Certificate][Set]')
    print(args)
    name = args['name']
    domain = args['domain']
    self.login.set_cdn_domain_sslcertificate(SetCdnDomainSSLCertificateRequest(
      cert_id = args['cert_id'],
      domain_name = f'{name}.{domain}',
      sslprotocol = args['sslprotocol'],
    ))
    DNS = CloudflareDNS(args['token'], domain=domain)
    DNS.delete(name=name, type='A')
    DNS.delete(name=name, type='CNAME')
    DNS.post(name=name, content=f'{name}.{domain}.w.cdngslb.com', type='CNAME')
