from . import *

class YamlRepository(AppInterfaceRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    class AppInterfaceDataMapper(i.AppInterface):

        class Options():
            roles = {
                'app.add_interface': blacklist('type'),
            }

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, interface_data: dict) -> AppInterfaceDataMapper:
        return self.AppInterfaceDataMapper(interface_data, strict=False)
    
    def get_interface(self, type: str) -> i.AppInterface:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces')
        interface_data = interfaces.get(type, None)
        if interface_data is None:
            return None
        
        # Add the interface to the list.
        return i.AppInterface(interface_data, strict=False)
    
    def save_interface(self, interface: i.AppInterface) -> None:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces', {})
        
        # Add new interface
        data = self._to_mapper(interface.to_primitive())
        interfaces['types'] = data.to_primitive()

        # Update the interfaces in the schema.
        data['interfaces'] = interfaces

        # Write the schema back to the file.
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)

        return