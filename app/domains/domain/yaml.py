import os, yaml

from ...constants import APP_CONFIGURATION_FILE
from .. import AppProject
from . import *

class YamlDomainService(DomainService):

    def __init__(self, app_project: AppProject):
        self.app_project = app_project

    def add_domain(self, key: str, name: str) -> DomainEntity:
        filepath = os.path.join(self.app_project.app_directory, APP_CONFIGURATION_FILE)
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        if data['domains'] is not None and key in data['domains']:
            return ('DOMAIN_ALREADY_EXISTS', key)
        if data['domains'] is None:
            data['domains'] = {key: {'name': name}}
        else:
            data['domains'][key] = {'name': name}
        with open(filepath, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'key': key,
            'name': name
        }
        return DomainEntity(raw_data=raw_data)