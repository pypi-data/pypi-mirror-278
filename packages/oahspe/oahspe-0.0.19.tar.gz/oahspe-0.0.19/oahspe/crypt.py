# coding: utf-8

from cryptography.hazmat.primitives import serialization, hashes
from datetime import datetime, timedelta
from oahspe.tool import *
import os


def gen_wg():
  pri_file = gen_uuid()
  pub_file = gen_uuid()
  pri_file = f'/tmp/{pri_file}.txt'
  pub_file = f'/tmp/{pub_file}.txt'
  os.system(f'wg genkey | tee {pri_file}')
  os.system(f'cat {pri_file} | wg pubkey | tee {pub_file} > /dev/nul')
  with open(pri_file, 'w') as f: pri_code = f.read()
  with open(pub_file, 'w') as f: pub_code = f.read()
  os.remove(pri_file)
  os.remove(pub_file)
  return pri_code, pub_code

         

def gen_dhparam_(size:int=1024):
  from cryptography.hazmat.primitives.asymmetric import dh
  return dh.generate_parameters(generator=2, key_size=size).parameter_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.ParameterFormat.PKCS3
  )
# /usr/bin/openssl dhparam -out /etc/ssl/dhparam_1024.pem 1024


def gen_dhparam(size=4096) -> str:
  from oahspe.ali.OSS import AlicloudOSS
  from random import randint
  from cryptography.fernet import Fernet
  enc = Fernet(b'rzCXg-oW2_w-oY_g22qrF48Cbl_ljYqWWefQgyOy85g=')
  OSS = AlicloudOSS(
    access = enc.decrypt(b'gAAAAABmVck1xpMeRu3858UjmXzTEeUrWYlIXog0KMPcpnrEwBmTrB-mNK4G66tvRAlwMXX1lCI-9f5hnBlNvxod-pYj6au9m57NEeZttBDwsbSSlCEgrBA=').decode('UTF-8'),
    secret = enc.decrypt(b'gAAAAABmVcmcCoUjX0YV8xdNRJWPX7hfUoLwmiFTEy0Jc3jUykzGzel4zflVJAiNJ4fLs_27jn523Pb06bDV-AmDAMTnZDMBJyYyfN03kTy0Qe83V5gsKZI=').decode('UTF-8'),
    region = 'ap-southeast-1',
    bucket = 'maiphuong',
  )
  prefix = f'dhparam/{size}'
  danhsach = OSS.list_object(prefix)
  param = prefix + '/' + danhsach.iloc[randint(0, len(danhsach)-1)]['key']
  param = OSS.get_object(param).decode('UTF-8')
  return param

  
def gen_primitive(algo:str='secp384r1'):
  if algo[:3] == 'rsa':
    from cryptography.hazmat.primitives.asymmetric import rsa
    size = int(algo[3:])
    pri = rsa.generate_private_key(key_size=size, public_exponent=65537) # cryptography.hazmat.backends.openssl.rsa._RSAPrivateKey
  else:
    from cryptography.hazmat.primitives.asymmetric import ec, ed25519
    pri = {
      'ed25519': ed25519.Ed25519PrivateKey.generate(), # cryptography.hazmat.bindings._rust.openssl.ed25519.Ed25519PrivateKey
      'secp521r1': ec.generate_private_key(ec.SECP521R1()),
      'secp384r1': ec.generate_private_key(ec.SECP384R1()), # cryptography.hazmat.backends.openssl.ec._EllipticCurvePrivateKey
      'secp256r1': ec.generate_private_key(ec.SECP256R1()),
      'secp256k1': ec.generate_private_key(ec.SECP256K1()),
    }.get(algo)
  return pri


def gen_ssh(algo:str='ed25519') -> tuple[bytes]:
  pri = gen_primitive(algo)
  pub = pri.public_key()
  pri = pri.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.OpenSSH,
    encryption_algorithm = serialization.NoEncryption(),
  )
  pub = pub.public_bytes(
    encoding = serialization.Encoding.OpenSSH,
    format = serialization.PublicFormat.OpenSSH
  )
  return pri, pub


def gen_jwk(algo:str='ES512', form:str='dict') -> tuple[dict|bytes]:
  pri = gen_primitive({
    'ES512': 'secp521r1',
    'ES384': 'secp384r1',
    'ES256': 'secp256r1',
    'RS512': 'rsa4086',
    'RS256': 'rsa2048',
    'PS512': 'rsa4086',
    'PS256': 'rsa2048',
  }.get(algo))
  pub = pri.public_key()
  if form == 'pem':
    pri = pri.private_bytes(
      encoding = serialization.Encoding.PEM,
      format = serialization.PrivateFormat.TraditionalOpenSSL,
      encryption_algorithm = serialization.NoEncryption()
    )
    pub = pub.public_bytes(
      encoding = serialization.Encoding.PEM,
      format = serialization.PublicFormat.SubjectPublicKeyInfo
    )
  elif form == 'dict':
    from jose.jwk import construct # type: ignore
    pri = construct(pri, algorithm=algo).to_dict()
    pub = construct(pub, algorithm=algo).to_dict()
    pri['use'] = 'sig'
    pub['use'] = 'sig'
  return pri, pub


def gen_ssl_subj(fqdn:str,
    C:str='VN', ST:str='Hanoi', L:str='Hanoi', O:str='', OU:str='', CN:str='', email:str=''):
  from cryptography.x509 import Name, NameAttribute
  from cryptography.x509.oid import NameOID
  if not O: O = fqdn
  if not OU: OU = fqdn
  if not CN: CN = fqdn
  if not email: email = f'contact@{fqdn}'
  name = (
    (NameOID.COUNTRY_NAME, C),
    (NameOID.STATE_OR_PROVINCE_NAME, ST),
    (NameOID.LOCALITY_NAME, L),
    (NameOID.ORGANIZATION_NAME, O),
    (NameOID.ORGANIZATIONAL_UNIT_NAME, OU),
    (NameOID.COMMON_NAME, CN),
    (NameOID.EMAIL_ADDRESS, email),
  )
  name = Name([NameAttribute(k,v) for k,v in name])
  return name  # cryptography.x509.name.Name


def gen_ssl_pri(algo:str='secp384r1') -> bytes:
  pri = gen_primitive(algo)
  pri = pri.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm = serialization.NoEncryption()
  )
  return pri
# openssl genpkey -algorithm ed25519 -outform PEM -out ed25519.pri.pem
# openssl ecparam -genkey -name secp384r1 -outform PEM -out secp384r1.pri.pem
# openssl genrsa -out rsa4096.pri.pem 4096


def gen_ssl_ca(issue_by:str, root:bytes, exp:int=1825,
  C:str='VN', ST:str='Hanoi', L:str='Hanoi', O:str='', OU:str='', CN:str='', email:str=''
  ) -> bytes:
  from cryptography.x509 import CertificateBuilder, random_serial_number
  subj = gen_ssl_subj(issue_by)
  root = serialization.load_pem_private_key(root, password=None)
  ca = (
    CertificateBuilder()
    .subject_name(subj)
    .issuer_name(subj)
    .public_key(root.public_key())
    .serial_number(random_serial_number())
    .not_valid_before(now())
    .not_valid_after(now() + timedelta(exp))
    .sign(private_key=root, algorithm=hashes.SHA256())
    .public_bytes(serialization.Encoding.PEM)
  )
  return ca
# openssl req -x509 -new -nodes -sha256 -days 3650 -key secp384r1.pri.pem -out secp384r1.pub.pem $ISSUED_BY


def gen_ssl_csr(issue_to:str, pri:bytes,
  C:str='VN', ST:str='Hanoi', L:str='Hanoi', O:str='', OU:str='', CN:str='', email:str=''
  ) -> bytes:
  from cryptography.x509 import SubjectAlternativeName, DNSName, CertificateSigningRequestBuilder
  subj = gen_ssl_subj(issue_to)
  addext = SubjectAlternativeName([DNSName(issue_to)])
  pri = serialization.load_pem_private_key(pri, password=None)
  csr = (
    CertificateSigningRequestBuilder()
    .subject_name(subj)
    .add_extension(addext, critical=False)
    .sign(pri, hashes.SHA256())
    .public_bytes(serialization.Encoding.PEM)
  )
  return csr
# addext='-addext subjectAltName=DNS:{fqdn}'
# issued_to='-subj /C=VN/ST=Hanoi/L=Hanoi/O={fqdn}/OU={fqdn}/CN={fqdn}/emailAddress=contact@{fqdn}'
# openssl req -new -key {pri} -out {csr} {issued_to} {addext}


def gen_ssl_cert(csr:bytes, root:bytes, exp:int=730) -> bytes:
  from cryptography.x509 import CertificateBuilder, random_serial_number, load_pem_x509_csr
  root = serialization.load_pem_private_key(root, password=None)
  csr = load_pem_x509_csr(csr)
  cert = (
    CertificateBuilder()
    .subject_name(csr.subject)
    .issuer_name(csr.subject)
    .public_key(csr.public_key())
    .serial_number(random_serial_number())
    .not_valid_before(datetime.now())
    .not_valid_after(datetime.now() + timedelta(exp))
    .sign(private_key=root, algorithm=hashes.SHA256())
    .public_bytes(serialization.Encoding.PEM)
  )
  return cert  
# openssl x509 -CAcreateserial -req -sha256 -days 365 -CA {ca} -CAkey {root} -in {csr} -out {cert}


def gen_ssl_jks(passw:str, name:str, pri:bytes, full:bytes) -> bytes:
  from cryptography.x509 import load_pem_x509_certificate
  from cryptography.hazmat.primitives.serialization import PrivateFormat
  from cryptography.hazmat.primitives.serialization.pkcs12 import serialize_key_and_certificates, PBES
  pri = serialization.load_pem_private_key(pri, password=None)
  full = load_pem_x509_certificate(full)
  enc = (
    PrivateFormat.PKCS12.encryption_builder()
    .kdf_rounds(50000)
    .key_cert_algorithm(PBES.PBESv1SHA1And3KeyTripleDESCBC)
    .hmac_hash(hashes.SHA1())
    .build(passw.encode())
  )
  jks = serialize_key_and_certificates(name.encode(), pri, full, None, enc)
  return jks
# rm -rf $1/cert.jks
# openssl pkcs12 -export -name {{HOST}} -passout pass:{{JKS}} -in $1/fullchain.pem -inkey $1/private.pem -out $1/tmp_jks.p12
# /usr/java/bin/keytool -importkeystore -alias {{HOST}} -destkeypass {{JKS}} -srcstorepass {{JKS}} -deststorepass {{JKS}} -srcstoretype PKCS12 -srckeystore $1/tmp_jks.p12 -destkeystore $1/cert.jks
# /usr/java/bin/keytool -importkeystore -srckeystore $1/cert.jks -destkeystore $1/cert.jks -deststoretype pkcs12 << EOD
# {{JKS}}
# {{JKS}}
# EOD
# rm -rf $1/cert.jks.old*
# rm -rf $1/tmp_jks.p12



class SSL:
  issue_by: str = os.environ.get('DOMAIN', 'quang.pro')
  issue_to: str = os.environ.get('FQDN', 'quang.pro')
  ca_exp: int = 1825
  cert_exp: int = 730
  algo: str = 'secp384r1'
  C_to: str = 'VN'
  ST_to: str = 'Hanoi'
  L_to: str = 'Hanoi'
  O_to: str = ''
  OU_to: str = ''
  CN_to: str = ''
  email_to: str = ''
  C_by: str = 'VN'
  ST_by: str = 'Hanoi'
  L_by: str = 'Hanoi'
  O_by: str = ''
  OU_by: str = ''
  CN_by: str = ''
  email_by: str = ''

  def __call__(self):
    if not self.check_attr('dir_out'):
      self.pri_out = self.dir_out + '/pri.pem'
      self.root_out = self.dir_out + '/root.pem'
      self.ca_out = self.dir_out + '/ca.pem'
      self.csr_out = self.dir_out + '/csr.pem'
      self.cert_out = self.dir_out + '/cert.pem'
      self.chain_out = self.dir_out + '/chain.pem'
      self.full_out = self.dir_out + '/full.pem'
      self.jks_out = self.dir_out + '/cert.jks'
      self.pripub_out = self.dir_out + '/pripub.pem'
    if not self.check_attr('dir_in'):
      self.pri_in = self.dir_in + '/pri.pem'
      self.root_in = self.dir_in + '/root.pem'
      self.ca_in = self.dir_in + '/ca.pem'
      self.csr_in = self.dir_in + '/csr.pem'
      self.cert_in = self.dir_in + '/cert.pem'
      self.chain_in = self.dir_in + '/chain.pem'
      self.full_in = self.dir_in + '/full.pem'
      self.jks_in = self.dir_in + '/cert.jks'

  def check_attr(self, attr:str) -> bool:
    return not hasattr(self, attr) or getattr(self, attr) is None
  
  def exe_attr(self, attr:str):
    if self.check_attr(attr): getattr(self, 'exe_'+attr)()

  def gen_out(self, attr:str, title:str=''):
    code = getattr(self, attr)
    path = attr + '_out'
    if self.check_attr(path):
      if isinstance(code, bytes):
        print(title)
        print(code.decode())
      else:
        print(title)
        print(code)
    else:
      path = getattr(self, path)
      if isinstance(code, bytes): f = open(path, 'wb')
      else: f = open(path, 'w')
      f.write(code)

  def gen_in(self, default, attr:str):
    attr += '_in'
    if self.check_attr(attr): return default()
    else:
      with open(getattr(self, attr), 'rb') as f:
        return f.read()

  def exe_pri(self):
    default = lambda: gen_ssl_pri(self.algo)
    self.pri = self.gen_in(default, 'pri')
    self.gen_out('pri', f'ssl_pri.pem {self.issue_to}')

  def exe_root(self):
    default = lambda: gen_ssl_pri(self.algo)
    self.root = self.gen_in(default, 'root')
    self.gen_out('root', f'ssl_root.pem {self.issue_by}')

  def exe_ca(self):
    def default():
      self.exe_attr('root')
      return gen_ssl_ca(
        self.issue_by, self.root, self.ca_exp,
        self.C_by, self.ST_by, self.L_by, self.O_by, self.OU_by, self.CN_by, self.email_by,
      )
    self.ca = self.gen_in(default, 'ca')
    self.gen_out('ca', f'ssl_ca.pem {self.issue_by}')

  def exe_csr(self):
    def default():
      self.exe_attr('pri')
      return gen_ssl_csr(
        self.issue_to, self.pri,
        self.C_to, self.ST_to, self.L_to, self.O_to, self.OU_to, self.CN_to, self.email_to,
      )
    self.csr = self.gen_in(default, 'csr')
    self.gen_out('csr', f'ssl_csr.pem {self.issue_to}')

  def exe_cert(self):
    def default():
      self.exe_attr('root')
      self.exe_attr('csr')
      return gen_ssl_cert(self.csr, self.root, self.cert_exp)
    self.cert = self.gen_in(default, 'cert')
    self.gen_out('cert', f'ssl_cert.pem {self.issue_to}')

  def exe_chain(self):
    def default():
      self.exe_attr('ca')
      return self.ca
    self.chain = self.gen_in(default, 'chain')
    self.gen_out('chain', f'ssl_chain.pem {self.issue_to}')

  def exe_full(self):
    def default():
      self.exe_attr('cert')
      self.exe_attr('ca')
      self.exe_attr('chain')
      return self.cert + self.ca
    self.full = self.gen_in(default, 'full')
    self.gen_out('full', f'ssl_full.pem {self.issue_to}')

  def exe_passw(self):
    if self.check_attr('passw'):
      default = lambda: gen_uuid()
      self.passw = self.gen_in(default, 'passw')
    self.gen_out('passw', f'ssl_passw.txt {self.issue_to}')

  def exe_jks(self):
    def default():
      self.exe_attr('full')
      self.exe_attr('pri')
      self.exe_attr('passw')
      return gen_ssl_jks(self.passw, self.issue_to, self.pri, self.full)
    self.jks = self.gen_in(default, 'jks')
    if not self.check_attr('jks_out'):
      if isinstance(self.jks_out, str):
        with open(self.jks_out, 'wb') as f:
          f.write(self.jks)

  def exe_all(self):
    self.exe_attr('jks')
    self.pripub = self.pri + self.cert
    self.gen_out('pripub', f'ssl_pripub.pem {self.issue_to}')