from . import *

class TypePropertiesDataMapper(StringTypeProperties, ListTypeProperties, DateTypeProperties):

    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist(),
            'map.str': whitelist('regex', 'min_length', 'max_length'),
            'map.list': whitelist('min_size', 'max_size'),
            'map.date': whitelist('formats'),
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
        # Return result if type properties is None
        if self.type_properties is None:
            return result
        # Map the type properties
        if self.type == 'str':
            result.type_properties = StringTypeProperties(self.type_properties.to_primitive('map.str'))
        elif self.type == 'list':
            result.type_properties = ListTypeProperties(self.type_properties.to_primitive('map.list'))
        elif self.type == 'date':
            result.type_properties = DateTypeProperties(self.type_properties.to_primitive('map.date'))
        # Return the result
        return result
    

class DomainModelDependencyDataMapper(DomainModelDependency):

    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist(),
        }

    def map(self) -> DomainModelDependency:
        return DomainModelDependency(self.to_primitive('map'))


class AppDomainModelDataMapper(AppDomainModel):

    properties = t.ListType(t.ModelType(DomainModelPropertyDataMapper), default=[])
    dependencies = t.ListType(t.ModelType(DomainModelDependencyDataMapper), default=[])
    
    class Options():
        roles = {
            'write': blacklist('id'),
            'map': blacklist('properties', 'dependencies'),
        }

    def map(self) -> AppDomainModel:
        result = AppDomainModel(self.to_primitive('map'))
        result.properties = [property.map() for property in self.properties]
        result.dependencies = [dependency.map() for dependency in self.dependencies]
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
    
    def get_domain_model(self, id: str) -> AppDomainModel:
        
        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # First check the value objects
        model_data = data['domain'].get('models', {})
        if id in model_data:
            mapper = self._to_mapper(AppDomainModelDataMapper, id=id, **model_data.get(id))
            return mapper.map()
        
        # Otherwise return None if no domain models are found.
        return None
    
    def get_domain_models(self, type: str = None) -> List[AppDomainModel]:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the value objects data
        model_data = data['domain'].get('models', {})

        # Return the value objects
        domain_models = [self._to_mapper(AppDomainModelDataMapper, id=id, **value_object).map() for id, value_object in model_data.items()]

        # Filter out type is specified
        if type is not None:
            domain_models = [domain_model for domain_model in domain_models if domain_model.type == type]

        # Return the domain models
        return domain_models

    def save_domain_model(self, domain_model: AppDomainModel) -> None:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the value objects data
        domain_model_data = data['domain'].get('models', {})

        # Create a data mapper from the value object
        domain_model_mapper = self._to_mapper(AppDomainModelDataMapper, **domain_model.to_primitive())

        # Set the required value of all model properties to None if they are False.
        for property in domain_model_mapper.properties:
            if property.required == False:
                property.required = None

        # Add the value object to the value objects data
        domain_model_data[domain_model.id] = domain_model_mapper.to_primitive('write')

        # Save the schema file data
        with open(self.schema_file_path, 'w') as stream:
            yaml.dump(data, stream)