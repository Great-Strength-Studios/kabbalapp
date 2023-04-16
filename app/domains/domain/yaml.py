import yaml

from . import *

class YamlDomainService(DomainService):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def add_domain(self, domain_key: str, domain_name: str) -> DomainEntity:
        with open(self.filepath, 'r') as f:
            data = yaml.safe_load(f)
        data['domains'].append({domain_key: {'name': domain_name}})
        with open(self.filepath, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'key': domain_key,
            'name': domain_name
        }
        return DomainEntity(raw_data=raw_data)