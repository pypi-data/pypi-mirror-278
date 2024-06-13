# coding: utf-8

class CloudflareSSL:
  def __init__(self, token, domain, access, secret, region, bucket):
    from oahspe.clf.DNS import CloudflareDNS
    from oahspe.ali.OSS import AlicloudOSS
    from oahspe.ali.CAS import AlicloudCAS
    self.domain = domain
    self.clf = CloudflareDNS(token, domain)
    self.oss = AlicloudOSS(
      access = access,
      secret = secret,
      region = region,
      bucket = bucket,
    )
    self.cas = AlicloudCAS(
      access = access,
      secret = secret,
      region = region,
    )

  

  def list_domain(self):
    danhsach = []
    for cert in self.oss.list_object('ssl')['prefix'].unique():
      cert = cert[4:].split('/')
      if len(cert) == 2 and cert[0] == self.domain:
        danhsach.append(cert[1])
    return danhsach


  def exists_domain(self, host):
    return host in self.list_domain()
  

  def delete_domain(self):
    self.oss.delete_prefix(f'ssl/{self.domain}')



  def put_cert_id(self, host, cert_id):
    self.oss.put_object(f'ssl/{self.domain}/{host}/cert_id.txt', cert_id)


  def get_cert_id(self, host):
    return int(self.oss.get_object(f'ssl/{self.domain}/{host}/cert_id.txt').decode('UTF-8'))


  def get_cert(self, host):
    return self.oss.get_object(f'ssl/{self.domain}/{host}/cert.pem').decode('UTF-8')


  def get_pri(self, host):
    return self.oss.get_object(f'ssl/{self.domain}/{host}/privkey.pem').decode('UTF-8')


  def get_chain(self, host):
    return self.oss.get_object(f'ssl/{self.domain}/{host}/chain.pem').decode('UTF-8')


  def _check_cert(self, cert:bytes, threshold=5):
    from cryptography.x509 import load_pem_x509_certificate
    from cryptography.hazmat.backends import default_backend
    from oahspe.tool import now
    cert = load_pem_x509_certificate(cert, default_backend())
    if (now() - cert.not_valid_before_utc).days > threshold:
      return False
    return True

  
  def check_cert(self, host, threshold=5):
    if not self.exists_domain(host): return False
    cert = self.oss.get_object(f'ssl/{self.domain}/{host}/cert.pem')
    return self._check_cert(cert, threshold)


  def upload_cert(self, host):
    from os import system
    if host == '@':
      prefix1 = f'/tmp/cert/live/{self.domain}'
    else:
      prefix1 = f'/tmp/cert/live/{host}.{self.domain}'
    prefix2 = f'ssl/{self.domain}/{host}'
    self.oss.put_file(f'{prefix1}/cert.pem', f'{prefix2}/cert.pem')
    self.oss.put_file(f'{prefix1}/privkey.pem', f'{prefix2}/privkey.pem')
    self.oss.put_file(f'{prefix1}/chain.pem', f'{prefix2}/chain.pem')
    self.oss.put_file(f'{prefix1}/fullchain.pem', f'{prefix2}/fullchain.pem')
    system('rm -rf /tmp/cert')


  def create_cert(self, host):
    from threading import Thread
    from time import sleep
    from os import system
    system('mkdir -p /tmp/cert')
    if host == '@':
      fqdn = self.domain
      acme_name = f'_acme-challenge.{self.domain}'
    else:
      acme_name = f'_acme-challenge.{host}'
      fqdn = f'{host}.{self.domain}'
    cmd = f'''\
    /code/env/bin/certbot certonly \
      --email no@thanks.com --agree-tos --no-eff-email \
      --force-renew -d {fqdn} \
      --cert-name {fqdn} \
      --key-type ecdsa --elliptic-curve secp384r1 \
      --redirect --hsts \
      --manual --preferred-challenges dns'''
    def thr1():
      sleep(5)
      with open('/tmp/cert/validation.txt', 'r') as f: acme_content = f.read()
      self.clf.delete(name=acme_name, type='TXT')
      self.clf.post(name=acme_name, type='TXT', content=acme_content)
    def thr2():
      system(cmd)
    t1 = Thread(target=thr1)
    t2 = Thread(target=thr2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    self.clf.delete(name=acme_name, type='TXT')


  def __call__(self, host):
    if not self.check_cert(host):
      self.create_cert(host)
      self.upload_cert(host)
