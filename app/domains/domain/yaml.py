import os, yaml

from ...constants import APP_CONFIGURATION_FILE
from .. import AppProject
from .core import *

class YamlDomainService(DomainService):

    def __init__(self, app_project: AppProject):
        self.app_project = app_project

    def add_domain(self, key: str, name: str) -> Domain:
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
        return Domain(raw_data=raw_data)
    
    def get_domain(self, key: str) -> Domain:
        filepath = os.path.join(self.app_project.app_directory, APP_CONFIGURATION_FILE)
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        if data['domains'] is not None and key in data['domains']:
            raw_data = {
                'key': key,
                'name': data['domains'][key]['name']
            }
            return Domain(raw_data=raw_data)
        else:
            return ('DOMAIN_NOT_FOUND', key)
    
    def add_domain_model(self, domain_key: str, key: str, name: str) -> DomainModel:
        filepath = os.path.join(self.app_project.app_directory, APP_CONFIGURATION_FILE)
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        if data['domains'] is not None and domain_key in data['domains']:
            if data['domains'][domain_key]['models'] is not None and key in data['domains'][domain_key]['models']:
                return ('DOMAIN_MODEL_ALREADY_EXISTS', key)
            if data['domains'][domain_key]['models'] is None:
                data['domains'][domain_key]['models'] = {key: {'name': name}}
            else:
                data['domains'][domain_key]['models'][key] = {'name': name}
        else:
            return ('DOMAIN_NOT_FOUND', domain_key)
        with open(filepath, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'name': name
        }
        return DomainModel(raw_data=raw_data)