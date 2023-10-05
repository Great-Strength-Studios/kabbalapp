from ...services import *
from .models import *

class YamlAppDomainService(AppDomainService):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def add_role(self, domain_key: str, key: str, role_type: str, role_fields: List[str]) -> AppDomainRole:
        import yaml
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
