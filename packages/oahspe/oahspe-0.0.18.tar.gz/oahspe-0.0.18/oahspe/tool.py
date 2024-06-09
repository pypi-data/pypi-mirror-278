# coding: utf-8

from pytz import timezone
from datetime import datetime
import os, hashlib, base64
import subprocess


def dir_ls(dir, depth=1):
  return {
    1: dir_ls1,
    2: dir_ls2,
    3: dir_ls3,
    4: dir_ls4,
    5: dir_ls5,
  }[depth](dir)


def dir_ls1(dir):
  folders, files = [], []
  for u in os.listdir(dir):
    if os.path.isdir(f'{dir}/{u}'):
      folders.append(u)
    else:
      files.append(u)
  return folders, files

def dir_ls2(dir):
  folders1, files = dir_ls1(dir)
  folders = []
  for struct in folders1:
    dir2 = f'{dir}/{struct}'
    folders2, files2 = dir_ls1(dir2)
    files2 = [f'{struct}/{file}' for file in files2]
    folders2 = [f'{struct}/{folder}' for folder in folders2]
    files.extend(files2)
    folders.extend(folders2)
  return folders, files

def dir_ls3(dir):
  folders1, files = dir_ls1(dir)
  folders = []
  for struct in folders1:
    dir2 = f'{dir}/{struct}'
    folders2, files2 = dir_ls2(dir2)
    files2 = [f'{struct}/{file}' for file in files2]
    folders2 = [f'{struct}/{folder}' for folder in folders2]
    files.extend(files2)
    folders.extend(folders2)
  return folders, files


def dir_ls4(dir):
  folders1, files = dir_ls1(dir)
  folders = []
  for struct in folders1:
    dir2 = f'{dir}/{struct}'
    folders2, files2 = dir_ls3(dir2)
    files2 = [f'{struct}/{file}' for file in files2]
    folders2 = [f'{struct}/{folder}' for folder in folders2]
    files.extend(files2)
    folders.extend(folders2)
  return folders, files


def dir_ls5(dir):
  folders1, files = dir_ls1(dir)
  folders = []
  for struct in folders1:
    dir2 = f'{dir}/{struct}'
    folders2, files2 = dir_ls4(dir2)
    files2 = [f'{struct}/{file}' for file in files2]
    folders2 = [f'{struct}/{folder}' for folder in folders2]
    files.extend(files2)
    folders.extend(folders2)
  return folders, files


def tmp_write(content):
  tmp = gen_uuid()
  tmp = f'/tmp/{tmp}'
  os.system('mkdir -p tmp')
  if isinstance(content, str):
    mode = 'w'
  else:
    content = to_byte(content)
    mode = 'wb'
  with open(tmp, mode) as f:
    f.write(content)
  return tmp


def checksum(content, chunk=100*1024*1024):
  from binascii import unhexlify
  content = to_byte(content)
  if len(content) <= chunk:
    return hashlib.md5(content).hexdigest()
  else:
    content = split_size(content, chunk)
    return hashlib.md5(b''.join([unhexlify(hashlib.md5(u).hexdigest()) for u in content])).hexdigest() + '-' + str(len(content))


def hash_any(content, algo='sha3_256') -> str:
  return getattr(hashlib, algo)(to_byte(content)).hexdigest()


def split_size(listin, num:int) -> list:
  return [listin[i:i+num] for i in range(0, len(listin), num)]


def split_count(listin, num:int) -> list:
  from math import ceil
  size = ceil(len(listin) / num)
  return [listin[i:i+size] for i in range(0, len(listin), size)]


def to_byte(data) -> bytes:
  if isinstance(data, bytes): return data
  if isinstance(data, str):
    if os.path.isdir(data):
      path = data
      path = tar(path)
      with open(path, 'rb') as f: data = f.read()
      os.remove(path)
      return data
    if os.path.isfile(data):
      with open(data, 'rb') as f: data = f.read()
      return data
  else:
    if hasattr(data, '__str__'):
      data = str(data)
    elif hasattr(data, '__dict__'):
      data = json_dump(data.__dict__)
  data = data.encode('UTF-8')
  return data


def encrypt_full(plain, key, b64=True, algo_hash='sha3_256', mode='GCM') -> bytes:
  key = to_byte(key)
  algo_hash = getattr(hashlib, algo_hash)
  if len(key) != algo_hash().digest_size: key = algo_hash(key).digest()
  plain = to_byte(plain)
  cipher = encrypt_byte(plain, key, mode)
  if b64: cipher = base64.b64encode(cipher)
  return cipher


def encrypt_byte(plain:bytes, key:bytes, mode='GCM') -> bytes:
  from Crypto.Cipher import AES
  from Crypto import Random
  bs = AES.block_size
  iv = Random.new().read(bs)
  bs = bs - len(plain) % bs
  mode = 'MODE_' + mode
  mode = getattr(AES, mode)
  cipher = iv + AES.new(key, mode, iv).encrypt(plain + bs*chr(bs).encode('UTF-8'))
  return cipher


def decrypt_full(enc, key, b64=True, algo_hash='sha3_256', mode='GCM') -> bytes:
  key = to_byte(key)
  algo_hash = getattr(hashlib, algo_hash)
  if len(key) != algo_hash().digest_size: key = algo_hash(key).digest()
  enc = to_byte(enc)
  if b64: enc = base64.b64decode(enc)
  return decrypt_byte(enc, key, mode)


def decrypt_byte(enc, key, mode='GCM') -> bytes:
  from Crypto.Cipher import AES
  mode = 'MODE_' + mode
  mode = getattr(AES, mode)
  plain = AES.new(key, mode, enc[:AES.block_size]).decrypt(enc[AES.block_size:])
  return plain[:-ord(plain[len(plain)-1:])]


def find_file(pattern, dir):
  import fnmatch
  res = []
  for root, dirs, files in os.walk(dir):
    for name in files:
      if fnmatch.fnmatch(name, pattern):
        res.append(os.path.join(root, name))
  return res


def gitignore(path='.gitignore'):
  if not os.path.isfile(path): return [], []
  with open(path , 'r') as f:
    content = f.read()
  content = content.splitlines()
  folder, file = [], []
  for obj in content:
    if obj:
      if obj[-1] == '/': folder.append(obj[:-1])
      else: file.append(obj)
  return folder, file


def untar(file):
  import tarfile
  os.system('mkdir -p tmp')
  name = file.split('/')[-1].split('.')
  name, ext = name[0], name[-1]
  with tarfile.open(file, f'r:{ext}') as f:
    f.extractall(f'tmp/{name}')



def tar(src, dst=None, type='bz2'):
  def func(target):
    if os.path.isdir(target): stream.add(target, '')
    else: stream.add(target, target.split('/')[-1])
  import tarfile
  os.system('mkdir -p tmp')
  if dst is None:
    dst = gen_uuid()[:16]
    dst = f'tmp/{dst}.tar.{type}'
  stream = tarfile.open(dst, f'w:{type}')
  if isinstance(src, str): func(src)
  else:
    for g in src: func(g)
  stream.close()
  return dst



def setdefault(args, pair):
  def _setdefault(key, value):
    if key not in args:
      args[key] = value
      return args
    old = args[key]
    if old is None or (isinstance(old, int|float) and old == 0) or (isinstance(old, set|tuple|list|str) and len(old) == 0):
      args[key] = value

  if isinstance(pair, dict):
    for k,v in pair.items():
      _setdefault(k, v)
  else:
    _setdefault(pair[0], pair[1])
  return args
  

def now(zone:str='Asia/Ho_Chi_Minh'):
  return _local(lambda: datetime.now(), zone)


def _local(time, zone:str='Asia/Ho_Chi_Minh'):
  zone = timezone(zone)
  return zone.normalize(timezone('UTC').localize(time()).astimezone(zone))


def local(time, zone:str='Asia/Ho_Chi_Minh'):
  if isinstance(time, int):
    time = datetime.fromtimestamp(time)
  zone = timezone(zone)
  return zone.normalize(timezone('UTC').localize(time).astimezone(zone))



def jinja(template, data):
  from jinja2 import Template
  if os.path.exists(template):
    with open(template, 'r') as f:
      template = f.read()
  return Template(template).render(**data)


def json_load(content):
  from ujson import loads
  if isinstance(content, bool):
    return {}
  try:
    with open(content, 'r') as f:
      content = f.read()
  except: pass
  try: content = loads(content)
  except: content = {}
  if not isinstance(content, dict):
    content = {}
  return content


def json_dump(dict, file=None):
  from ujson import dumps
  if file is None:
    try: res = dumps(dict, indent=2)
    except: res = dumps({})
  else:
    try: res = dumps(dict, separators=(',', ':'))
    except: res = dumps({})
    with open(file, 'w') as f:
      f.write(res)
  return res


def json_write(file, key, value):
  res = json_load(file)
  res[key] = value
  json_dump(res, file)


def yml_load(content):
  from yaml import safe_load
  if isinstance(content, bool):
    return {}
  try:
    with open(content, 'r') as f:
      content = f.read()
  except: pass
  try:
    content = safe_load(content)
  except:
    content = {}
  if not isinstance(content, dict):
    content = {}
  return content


def yml_dump(dict, file=None):
  from yaml import safe_dump
  try: res = safe_dump(dict, indent=2)
  except: res = safe_dump({})
  if file is not None:
    with open(file, 'w') as f:
      f.write(res)
  return res


def yml_write(file, key, value):
  res = yml_load(file)
  res[key] = value
  yml_dump(res, file)


def csv_load(content):
  import pandas as pd
  if os.path.exists(content):
    if content[-3:] == 'tsv':
      content = pd.read_csv(content, delimiter='\t')
    else:
      content = pd.read_csv(content)
  else:
    try:
      content = [row.split(',') for row in content.splitlines()]
      content = pd.DataFrame(content)
    except:
      content = pd.DataFrame({})
  return content
  

def parse_key(key):
  if '/' not in key:
    prefix = ''
  else:
    prefix = key.split('/')
    key = prefix[-1]
    prefix = '/'.join(prefix[:-1])
  return key, prefix


def gen_uuid(size:int=64, punc:str='') -> str:
  from random import choice
  from string import ascii_letters, digits

  def check(mess:str) -> bool:
    check_digits = False
    for ch in mess:
      if ch in digits:
        check_digits = True
        break
    if punc == '': check_punc = True
    else:
      check_punc = False
      for ch in mess:
        if ch in punc:
          check_punc = True
          break
    return check_digits and check_punc

  pool = ascii_letters + digits + punc
  size = size - 1
  def rand() -> str:
    return [choice(pool) for _ in range(size)]

  first = choice(ascii_letters)
  uuid = rand()
  while not check(uuid): uuid = rand()
  uuid = ''.join(uuid)
  uuid = first + uuid
  return uuid


def bash(code):
  code = '#!/usr/bin/bash\n' + code
  sh = tmp_write(code)
  os.system(f'chmod +x {sh}')
  try: os.system(f'/usr/bin/bash {sh}')
  finally: os.remove(sh)

def cmd_out(code):
  return subprocess.check_output(code.split(' ')).decode('UTF-8')

def bash_out(code):
  code = '#!/usr/bin/bash\n' + code
  sh = tmp_write(code)
  os.system(f'chmod +x {sh}')
  try: res = subprocess.check_output(['/bin/bash', sh]).decode('UTF-8')
  finally: os.remove(sh)
  return res

def output(code:str|bytes, path:str|None=None, title:str=''):
  if path is None:
    if isinstance(code, bytes):
      print(title)
      print(code.decode())
    else:
      print(title)
      print(code)
  else:
    if isinstance(code, bytes): f = open(path, 'wb')
    else: f = open(path, 'w')
    f.write(code)


def qrcode(text):
  '''max=1273'''
  from qrcode import QRCode, constants
  qr = QRCode(
    version=1,
    error_correction=constants.ERROR_CORRECT_H,
    box_size=10,
    border=4,
  )
  qr.add_data(text)
  qr.make(fit=True)
  img = qr.make_image(fill='black', back_color='white')
  return img
