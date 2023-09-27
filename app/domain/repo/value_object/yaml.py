from . import *


class ValueObjectDataMapper(ValueObject):
    
    class Options():
        roles = {
            'write': blacklist('id'),
            'map': blacklist(),
        }
        serialize_when_none = False

    def map(self) -> ValueObject:
        return ValueObject(self.to_primitive('map'))
    

class YamlRepository(ValueObjectRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, mapper_type: type, **data):
        return mapper_type(data, strict=False)
    
    def get_value_object(self, id: str) -> ValueObject:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.load(stream)

        # Get the value objects data
        value_object_data = data['domain'].get('value_objects', {})

        # Loop through the value objects data and return the value object if found
        for object_id, value_object in value_object_data.items():
            if id == object_id:
                return self._to_mapper(ValueObjectDataMapper, id=object_id, **value_object).map()
        
        # If no value object was found, return None
        return None

    def save_value_object(self, value_object: ValueObject) -> None:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.load(stream)

        # Get the value objects data
        value_object_data = data['domain'].get('value_objects', {})

        # Create a data mapper from the value object
        value_object_mapper = self._to_mapper(ValueObjectDataMapper, **value_object.to_primitive())

        # Add the value object to the value objects data
        value_object_data[value_object.id] = value_object_mapper.to_primitive('write')

        # Save the schema file data
        with open(self.schema_file_path, 'w') as stream:
            yaml.dump(data, stream)