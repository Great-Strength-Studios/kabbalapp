import os, yaml

from .. import *

class YamlAppDomainService(AppDomainService):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        return os.path.join(self.app_directory, self.schema_location)

    def add_domain(self, key: str, name: str, aliases: List[str]) -> AppDomain:
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        domain_data = { 'name': name, 'aliases': aliases }
        try:
            if data['domains'] is not None and key in data['domains']:
                return ('DOMAIN_ALREADY_EXISTS', key)
            if data['domains'] is None:
                data['domains'] = {key: domain_data}
            else:
                data['domains'][key] = domain_data
        except KeyError:
            data['domains'] = {key: domain_data}
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'key': key,
            'name': name
        }
        return AppDomain(raw_data=raw_data)
    
    def get_domain(self, key: str) -> AppDomain:
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        if data['domains'] is not None and key in data['domains']:
            raw_data = {
                'key': key,
                'name': data['domains'][key]['name']
            }
            return AppDomain(raw_data=raw_data)
        else:
            return ('DOMAIN_NOT_FOUND', key)
    
    def add_model(self, domain_key: str, key: str, name: str, class_name: str) -> AppDomainModel:
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        model_data = {'name': name, 'class_name': class_name}
        if data['domains'] is not None and domain_key in data['domains']:
            try:
                if data['domains'][domain_key]['models'] is not None and key in data['domains'][domain_key]['models']:
                    return ('DOMAIN_MODEL_ALREADY_EXISTS', key)
                if data['domains'][domain_key]['models'] is None:
                    data['domains'][domain_key]['models'] = {key: model_data}
                else:
                    data['domains'][domain_key]['models'][key] = model_data
            except KeyError:
                data['domains'][domain_key]['models'] = {key: model_data}
        else:
            return ('DOMAIN_NOT_FOUND', domain_key)
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'name': name,
            'class_name': class_name
        }
        return AppDomainModel(raw_data=raw_data)
    
    def add_role(self, domain_key: str, key: str, role_type: str, role_fields: List[str]) -> AppDomainRole:
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        role_data = {'type': role_type, 'fields': role_fields}
        if data['domains'] is not None and domain_key in data['domains']:
            try:
                if data['domains'][domain_key]['roles'] is not None and key in data['domains'][domain_key]['roles']:
                    return ('DOMAIN_ROLE_ALREADY_EXISTS', key)
                if data['domains'][domain_key]['roles'] is None:
                    data['domains'][domain_key]['roles'] = {key: role_data}
                else:
                    data['domains'][domain_key]['roles'][key] = role_data
            except KeyError:
                data['domains'][domain_key]['roles'] = {key: role_data}
        else:
            return ('DOMAIN_NOT_FOUND', domain_key)
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'type': role_type,
            'fields': role_fields
        }
        return AppDomainRole(raw_data=raw_data)