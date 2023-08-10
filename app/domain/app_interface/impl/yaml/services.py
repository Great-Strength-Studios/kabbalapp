from ...services import *
from .models import *

class YamlAppInterfaceService(AppInterfaceService):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def add_interface(self, key: str) -> None:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        interface_data = {}
        try:
            if data['interfaces'] is not None and key in data['interfaces']:
                return ('INTERFACE_ALREADY_EXISTS', key)
            if data['interfaces'] is None:
                data['interfaces'] = {key: interface_data}
            else:
                data['interfaces'][key] = interface_data
        except KeyError:
            data['interfaces'] = {key: interface_data}
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        return None