from . import *

class TypePropertiesDataMapper(TypeProperties):

    regex = t.StringType()
    min_length = t.IntType()
    max_length = t.IntType()
    min_size = t.IntType()
    max_size = t.IntType()

    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist(),
            'map.str': whitelist('regex', 'min_length', 'max_length'),
            'map.list': whitelist('min_size', 'max_size'),
        }
        serialize_when_none = False

    def map(self) -> TypeProperties:
        return TypeProperties(self.to_primitive('map'))

class DomainModelPropertyDataMapper(DomainModelProperty):

    type_properties = t.ModelType(TypePropertiesDataMapper, default=None)

    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist('type_properties'),
        }
        serialize_when_none = False

    def map(self) -> DomainModelProperty:
        # Create the result
        result = DomainModelProperty(self.to_primitive('map'))
        # Map the type properties
        if self.type == 'str':
            result.type_properties = StringTypeProperties(self.type_properties.to_primitive('map.str'))
        elif self.type == 'list':
            result.type_properties = ListTypeProperties(self.type_properties.to_primitive('map.list'))
        # Return the result
        return result


class ValueObjectDataMapper(ValueObject):

    properties = t.ListType(t.ModelType(DomainModelPropertyDataMapper), default=[])
    
    class Options():
        roles = {
            'write': blacklist('id'),
            'map': blacklist('properties'),
        }

    def map(self) -> ValueObject:
        result = ValueObject(self.to_primitive('map'))
        result.properties = [property.map() for property in self.properties]
        return result
    

class YamlRepository(DomainRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, mapper_type: type, **data):
        return mapper_type(data, strict=False)
    
    def get_domain_model(self, id: str) -> ValueObject:
        
        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # First check the value objects
        value_object_data = data['domain'].get('value_objects', {})
        if id in value_object_data:
            mapper = self._to_mapper(ValueObjectDataMapper, id=id, **value_object_data.get(id))
            return mapper.map()
        
        # Otherwise return None if no domain models are found.
        return None
    
    def get_value_objects(self) -> List[ValueObject]:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the value objects data
        value_object_data = data['domain'].get('value_objects', {})

        # Return the value objects
        return [self._to_mapper(ValueObjectDataMapper, id=id, **value_object).map() for id, value_object in value_object_data.items()]


    def save_value_object(self, value_object: ValueObject) -> None:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the value objects data
        value_object_data = data['domain'].get('value_objects', {})

        # Create a data mapper from the value object
        value_object_mapper = self._to_mapper(ValueObjectDataMapper, **value_object.to_primitive())

        # Add the value object to the value objects data
        value_object_data[value_object.id] = value_object_mapper.to_primitive('write')

        # Save the schema file data
        with open(self.schema_file_path, 'w') as stream:
            yaml.dump(data, stream)