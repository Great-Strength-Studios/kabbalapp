import os, yaml

from ...constants import APP_CONFIGURATION_FILE
from .. import AppProject
from . import *

class YamlDomainService(DomainService):

    def __init__(self, app_project: AppProject):
        self.app_project = app_project

    def add_domain(self, domain_key: str, domain_name: str) -> DomainEntity:
        filepath = os.path.join(self.app_project.app_directory, APP_CONFIGURATION_FILE)
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        data['domains'].append({domain_key: {'name': domain_name}})
        with open(self.filepath, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'key': domain_key,
            'name': domain_name
        }
        return DomainEntity(raw_data=raw_data)