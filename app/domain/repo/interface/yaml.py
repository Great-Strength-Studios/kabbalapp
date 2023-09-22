from . import *

class YamlRepository(AppInterfaceRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def add_interface(self, interface: i.AppInterface) -> None:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces', [])
        
        # Check to see if the interface already exists.
        existing_interfaces = [i for i in interfaces if i['type'] == interface.type]
        if existing_interfaces:
            return ('INTERFACE_ALREADY_EXISTS', interface.type)
        
        # Add the interface to the list.
        interfaces.append(interface.to_primitive())

        # Write the schema back to the file.
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)

        return