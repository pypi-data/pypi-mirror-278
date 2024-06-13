import os, sys
from oahspe.tool import now, bash

class Exe:
  def __init__(self, path:str, mode):
    self.os = os.name
    if self.os == 'nt': self.sep = '\\'
    elif self.os == 'posix': self.sep = '/'
    self.path = path
    self.cwd = os.getcwd()
    self.path_break()
    self.mode = str(mode).strip()
    {
      'py': self.exe_py,
      '': self.exe_bin,
      'bin': self.exe_bin,
      'sh': self.exe_sh,
      'zsh': self.exe_zsh,
      'java': self.exe_java,
      'class': self.exe_class,
      'jar': self.exe_jar,
      'cpp': self.exe_cpp,
      'js': self.exe_js,
      'ts': self.exe_ts,
      'go': self.exe_go,
      'php': self.exe_php,
      'rb': self.exe_rb,
      'rs': self.exe_rs,
      'scala': self.exe_scala,
      'pl': self.exe_pl,
      'jl': self.exe_jl,
      'lua': self.exe_lua,
      'r': self.exe_r,
      'kt': self.exe_kt,
      'cs': self.exe_cs,
      'csx': self.exe_cs,
      'hs': self.exe_hs,
      'dart': self.exe_dart,
      'exs': self.exe_exs,
      'star': self.exe_star,
      'pyx': self.exe_pyx,
      'txt': self.exe_txt,
      'md': self.exe_md,
      'rst': self.exe_rst,
      'json': self.exe_json,
      'yml': self.exe_yml,
      'pem': self.exe_pem,
      'tf': self.exe_tf,
    }[self.ext]()

  def path_break(self):
    tmp = self.path.split(self.sep)
    self.folder = self.sep.join(tmp[:-1])
    self.fullname = tmp[-1]
    tmp = self.fullname.split('.')
    if len(tmp) > 1:
      self.name = tmp[0]
      self.ext = tmp[-1]
      self.fullext = '.'.join(tmp[1:])
      self.leftext = '.'.join(tmp[1:-1])
      self.leftname = self.name
      if self.leftext != '': self.leftname += '.' + self.leftext
      self.bin = self.folder + self.sep + self.leftname + '.bin'
    else:
      tmp = tmp[0]
      self.name = tmp
      self.fullname = tmp
      self.leftname = tmp
      self.ext = ''
      self.fullext = ''
      self.leftext = ''
      self.bin = self.path + '.bin'
  
  def pre_get(self, commend:str='#'):
    with open(self.path, 'r') as f:
      lines = f.readlines()
    cmd = []
    shebang = []
    len_commend = len(commend)
    for line in lines:
      line = line.strip()
      if line == '': continue
      elif line[:2] == '#!':
        shebang.append(line[2:].strip())
      elif line[:len_commend] == commend:
        cmd.append(line[len_commend:].strip())
      else: break
    self.pre_cmd = '.'.join(cmd)
    if shebang: self.pre_shebang = shebang[0]
    else: self.pre_shebang = shebang
    
  
  def exe_py(self):
    # if self.os == 'posix':
      # self.pre_get('#')
      # bash(self.pre_cmd)
    py = sys.executable
    os.system(f'{py} {self.path}')


  def exe_bin(self):
    os.system(self.path)
  
  def exe_sh(self):
    sh = os.environ.get('SHELL', '/usr/bin/sh')
    os.system(f'chmod +x {self.path}')
    os.system(f'{sh} {self.path}')

  def exe_zsh(self):
    if os.path.isfile('/usr/bin/zsh'):
      sh = '/usr/bin/zsh'
    else:
      sh = os.environ.get('SHELL', '/usr/bin/sh')
    os.system(f'chmod +x {self.path}')
    os.system(f'{sh} {self.path}')

  def env_java(self):
    java = os.environ.get('JAVA_HOME', None)
    if java is None: return None
    else: 
      self.java = java + self.sep + 'bin' + self.sep + 'java'
      self.javac = java + self.sep + 'bin' + self.sep + 'javac'

  def exe_java(self):
    self.env_java()
    os.chdir(self.folder)
    os.system(f'{self.javac} {self.fullname}')
    if self.mode == '1': os.system(f'{self.java} {self.leftname}')
    os.chdir(self.cwd)

  def exe_class(self):
    self.env_java()
    os.chdir(self.folder)
    os.system(f'{self.java} {self.leftname}')
    os.chdir(self.cwd)

  def exe_jar(self):
    self.env_java()
    os.system(f'{self.java} {self.path}')

  def exe_cpp(self):
    os.system(f'g++ -o {self.bin} {self.path}')
    if self.mode == '1': os.system(self.bin)

  def exe_js(self):
    self.pre_get('//')
    bash(self.pre_cmd)
    os.system(f'node {self.path}')

  def exe_ts(self):
    os.system(f'tsc {self.path}')
    if self.mode == '1':
      js = self.path[:-3] + '.js'
      self.pre_get('//')
      bash(self.pre_cmd)
      os.system(f'node {js}')

  def exe_go(self):
    # os.system(f'go run {self.path}')
    os.system(f'go build -o {self.bin} {self.path}')
    if self.mode == '1': os.system(self.bin)
  
  def exe_php(self):
    os.system(f'php {self.path}')

  def exe_rb(self):
    self.pre_get('#')
    bash(self.pre_cmd)
    os.system(f'ruby {self.path}')

  def exe_rs(self):
    os.system(f'rustc -o {self.bin} {self.path}')
    if self.mode == '1': os.system(self.bin)

  def exe_scala(self):
    os.chdir(self.folder)
    os.system(f'scalac {self.fullname}')
    if self.mode == '1': os.system(f'scala {self.leftname}')
    os.chdir(self.cwd)

  def exe_pl(self):
    os.system(f'/usr/bin/perl {self.path}')

  def exe_jl(self):
    self.pre_get('#')
    bash(self.pre_cmd)
    os.system(f'julia {self.path}')

  def exe_lua(self):
    self.pre_get('--')
    bash(self.pre_cmd)
    os.system(f'lua {self.path}')

  def exe_r(self):
    self.pre_get('#')
    bash(self.pre_cmd)
    os.system(f'Rscript {self.path}')

  def exe_kt(self):
    os.chdir(self.folder)
    os.system(f'kotlinc -include-runtime {self.fullname} -d {self.leftname}.jar')
    if self.mode == '1':
      self.env_java()
      os.system(f'{self.java} -jar {self.leftname}.jar')
    os.chdir(self.cwd)

  def exe_cs(self):
    os.system(f'dotnet-script {self.path}')

  def exe_hs(self):
    # os.system(f'runhaskell {self.path}')
    os.chdir(self.folder)
    os.system(f'ghc {self.fullname}')
    if self.mode == '1': os.system(f'.{self.sep}{self.leftname}')
    os.chdir(self.cwd)

  def exe_dart(self):
    os.system(f'dart {self.path}')

  def exe_exs(self):
    os.system(f'elixir {self.path}')

  def exe_star(self):
    from starlark_go import Starlark # type: ignore
    Starlark().exec(open(self.path, 'r').read())

  def exe_pyx(self):
    from setuptools import setup
    from Cython.Build import cythonize # type: ignore
    sys.argv[1] = 'build_ext'
    sys.argv[2] = '--inplace'
    os.chdir(self.folder)
    setup(ext_modules=cythonize(self.fullname))
    os.chdir(self.cwd)

  def exe_txt(self):
    if 'requirement' in self.fullname:
      py = sys.executable
      os.system(f'{py} -m pip install --upgrade --no-cache-dir --no-warn-script-location --break-system-packages -r {self.path}')

  def exe_md(self):
    if 'README' in self.fullname:
      prefix = f'git --git-dir={self.folder}/.git --work-tree={self.folder}'
      fqdn = os.environ.get('FQDN', '')
      if self.mode == '1': os.system(f'{prefix} rm -r --cached .')
      os.system(f'{prefix} add .')
      os.system(f'{prefix} commit -m "{fqdn} {now()}"')
      os.system(f'{prefix} push')

  def exe_rst(self):
    if 'README' in self.fullname:
      prefix = f'git --git-dir={self.folder}/.git --work-tree={self.folder}'
      fqdn = os.environ.get('FQDN', '')
      if self.mode == '1': os.system(f'{prefix} rm -r --cached .')
      os.system(f'{prefix} add .')
      os.system(f'{prefix} commit -m "{fqdn} {now()}"')
      os.system(f'{prefix} push')

  def exe_yml(self):
    with open(self.path, 'r') as f:
      content = f.read()
    if 'tasks:' in content and 'hosts:' in content:
      os.system(f'ansible-playbook -i /home/vt_admin/.ssh/hosts.yml {path}')
    # if self.mode == '1': os.system(f'kubectl apply -f {self.path}')
    # elif self.mode == '2': os.system(f'kubectl delete -f {self.path}')

  def exe_tf(self):
    os.chdir('/code')
    if self.mode == '1':
      bash(f'''
terraform -chdir={self.folder} init -upgrade
terraform -chdir={self.folder} fmt
terraform -chdir={self.folder} validate
''')
      
    elif self.mode == '2':
      bash(f'''
terraform -chdir={self.folder} init -upgrade
terraform -chdir={self.folder} fmt
terraform -chdir={self.folder} validate
terraform -chdir={self.folder} apply -auto-approve
''')
    elif self.mode == '3':
      bash(f'''
terraform -chdir={self.folder} destroy -auto-approve
sudo umount -lf nas
sudo rm -rf nas
sudo umount -lf oss
sudo rm -rf oss
sudo wg-quick down wg0
''')
    os.chdir(self.cwd)

  def exe_pem(self):
    if self.mode == '1': os.system(f'chmod 700 {self.path}')
    elif self.mode == '2': os.system(f'chmod 740 {self.path}')

  def exe_json(self):
    if 'package' in self.fullname:
      os.chdir(self.folder)
      os.system('npm run build')
      os.chdir(self.cwd)


path, mode, *_ = sys.argv[1:]
Exe(path, mode)
