from . import *


class AppInterfaceTypeDataMapper(AppInterfaceType):

    class Options():
        roles = {
            'write': blacklist('type'),
        }

    def map(self):
        return AppInterfaceType(self.to_primitive())
    

class YamlRepository(AppInterfaceRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, **data) -> AppInterfaceTypeDataMapper:
        return AppInterfaceTypeDataMapper(data, strict=False)
    
    def get_interfaces(self) -> AppInterfaceType:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces')
        interface_data = interfaces.get('types', {})
        
        # Return list of mapped interface types
        return [self._to_mapper(**i, type=type).map() for type, i in interface_data.items()]
    
    def save_interface_type(self, interface: AppInterfaceType) -> None:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces', {})
        
        # Add new interface
        mapper = self._to_mapper(**interface.to_primitive())
        interfaces['types'][mapper.type] = mapper.to_primitive('write')

        # Update the interfaces in the schema.
        data['interfaces'] = interfaces

        # Write the schema back to the file.
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)

        return