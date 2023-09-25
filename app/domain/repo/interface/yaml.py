from . import *

class YamlRepository(AppInterfaceRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    class AppInterfaceTypeDataMapper(i.AppInterfaceType):

        class Options():
            roles = {
                'write': blacklist('type'),
            }

        def map(self):
            return i.AppInterfaceType(self.to_primitive())

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, **data) -> AppInterfaceTypeDataMapper:
        return self.AppInterfaceTypeDataMapper(data, strict=False)
    
    def get_interfaces(self) -> i.AppInterfaceType:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces')
        interface_data = interfaces.get('types', {})
        
        # Return list of mapped interface types
        return [self._to_mapper(**i, type=type).map() for type, i in interface_data.items()]
    
    def save_interface_type(self, interface: i.AppInterfaceType) -> None:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces', {})
        
        # Add new interface
        data = self._to_mapper(interface.to_primitive())
        interfaces['types'][data.type] = data.to_primitive('write')

        # Update the interfaces in the schema.
        data['interfaces'] = interfaces

        # Write the schema back to the file.
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)

        return