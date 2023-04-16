import yaml

from . import *

class YamlDomainService(DomainService):

    def __init__(self, filepath: str):
        self.filepath = filepath

    def add_domain(self, domain_name: str) -> DomainEntity:
        with open(self.filepath, 'r') as f:
            data = yaml.safe_load(f)
        data['domains'].append({'name': domain_name})
        with open(self.filepath, 'w') as f:
            yaml.dump(data, f)