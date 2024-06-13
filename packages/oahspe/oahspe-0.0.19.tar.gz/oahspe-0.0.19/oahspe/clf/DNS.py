class CloudflareDNS:
  def __init__(self, token, domain):
    from CloudFlare import CloudFlare
    self.domain = domain
    cf = CloudFlare(token=token)
    for zone in cf.zones.get():
      if zone['name'] == domain:
        self.login = cf
        self.zone_id = zone['id']
        break
  

  def post(self, name, content, type):
    self.login.zones.dns_records.post(self.zone_id, data={
      'name': name,
      'content': content,
      'type': type,
    })
  

  def _get(self, name, type):
    return [dns for dns in self.login.zones.dns_records.get(self.zone_id, params={'name': f'{name}.{self.domain}'}) if dns['type'] == type]


  def get(self, name, type):
    return [dns['content'] for dns in self._get(name, type)]
  

  def delete(self, name, type):
    return [self.login.zones.dns_records.delete(self.zone_id, dns['id']) for dns in self._get(name, type)]
  
