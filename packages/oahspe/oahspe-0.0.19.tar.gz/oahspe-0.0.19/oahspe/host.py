# coding: utf-8

with open('~/.ssh/static.txt', 'r') as f: static_ssh = f.read()
def text_strip1(text:str):
  text = text.strip()
  while '\n\n' in text:
    text = text.replace('\n\n', '\n')
  return text

def hosts_import(text:str='~/.ssh/config'):
  with open(text, 'r') as f:
    content = f.read()
  res = {}
  for block in text_strip1(content).split('Host ')[1:]:
    info = {}
    block = block.strip().splitlines()
    for row in block[1:]:
      row = row.strip()
      while '  ' in row:
        row = row.replace('  ', ' ')
      row = row.strip().split(' ')
      info[row[0]] = row[1]
    res[block[0]] = info
  if '*' in res:
    del res['*']
  return res

def hosts_ini(group:dict, hosts:dict=hosts_import()):
  res = ''
  group_text = {k:f'\n[{k}]\n' for k in group.keys()}
  for host, info in hosts.items():
    row = f'{info['Hostname']} ansible_ssh_private_key_file={info['IdentityFile']} ansible_user={info['User']} ansible_port={info['Port']}\n'
    if host != 'github.com':
      res += f'[{host}]\n{row}'
    for k,v in group.items():
      if host in v:
        group_text[k] += row
  res = text_strip1(res + ''.join(group_text.values()))
  return res

def hosts_yml(group:dict, hosts:dict=hosts_import()):
  res = ''
  group_text = {k:f'\n{k}:\n  hosts:\n' for k in group.keys()}
  for host, info in hosts.items():
    row = f'''\
    {info['Hostname']}:
      ansible_ssh_private_key_file: {info['IdentityFile']}
      ansible_user: {info['User']}
      ansible_port: {info['Port']}
'''
    if host != 'github.com':
      res += f'{host}:\n  hosts:\n{row}'
    for k,v in group.items():
      if host in v:
        group_text[k] += row
  res = text_strip1(res + ''.join(group_text.values()))
  return res

def hosts_txt(hosts:dict=hosts_import()):
  return static_ssh + '\n\n' + '\n'.join([f'Host {host}\n' + '\n'.join([f'  {k} {v}' for k,v in info.items()]) for host,info in hosts.items()]) + '\n'
