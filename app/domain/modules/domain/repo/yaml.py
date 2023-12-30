from . import *

class TypePropertiesDataMapper(StringTypeProperties, ListTypeProperties, DateTypeProperties, DateTimeTypeProperties, DictTypeProperties):

    convert_tz = t.BooleanType()
    drop_tzinfo = t.BooleanType()
    tzd = t.StringType()

    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist(),
            'map.str': whitelist('regex', 'min_length', 'max_length'),
            'map.list': whitelist('min_size', 'max_size'),
            'map.date': whitelist('formats'),
            'map.datetime': whitelist('formats', 'serialized_format', 'parser', 'tzd', 'convert_tz', 'drop_tzinfo'),
            'map.dict': whitelist('coerce_key'),
        }
        serialize_when_none = False

    def map(self) -> TypeProperties:
        return TypeProperties(self.to_primitive('map'))

class DomainModelAttributeDataMapper(DomainModelAttribute):

    type_properties = t.ModelType(TypePropertiesDataMapper, default=None)

    class Options():
        roles = {
            'write': blacklist('parent_model_id'),
            'map': blacklist('type_properties'),
        }
        serialize_when_none = False

    def map(self, **kwargs) -> DomainModelAttribute:
        # Create the result
        result = DomainModelAttribute(self.to_primitive('map'))

        # Set the kwargs 
        # TODO - Put this in the mapper kabbalapp core base class.
        for attribute, value in kwargs.items():
            setattr(result, attribute, value)

        # Return result if type properties is None
        if self.type_properties is None:
            return result
        # Map the type properties
        if self.type == STR_TYPE:
            result.type_properties = StringTypeProperties(self.type_properties.to_primitive('map.str'))
        elif self.type == LIST_TYPE:
            result.type_properties = ListTypeProperties(self.type_properties.to_primitive('map.list'))
        elif self.type == DICT_TYPE:
            result.type_properties = DictTypeProperties(self.type_properties.to_primitive('map.dict'))
        elif self.type == DATE_TYPE:
            result.type_properties = DateTypeProperties(self.type_properties.to_primitive('map.date'))
        elif self.type == DATETIME_TYPE:
            result.type_properties = DateTimeTypeProperties(self.type_properties.to_primitive('map.datetime'))

            
        # Return the result
        return result
    

class DomainModelDependencyDataMapper(DomainModelDependency):

    class Options():
        roles = {
            'write': blacklist('name', 'description'),
            'map': blacklist(),
        }

    def map(self) -> DomainModelDependency:
        return DomainModelDependency(self.to_primitive('map'))
    

class DomainMethodParameterDataMapper(DomainMethodParameter):
    '''Data mapper for DomainMethodParameter
    
    '''

    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist(),
        }
        serialize_when_none = False

    def map(self) -> DomainMethodParameter:
        return DomainMethodParameter(self.to_primitive('map'))

class DomainMethodDataMapper(DomainMethod):

    parameters = t.ListType(t.ModelType(DomainMethodParameterDataMapper), default=[])
    
    class Options():
        roles = {
            'write': blacklist('method_name'),
            'map': blacklist('parameters'),
        }
        serialize_when_none = False

    def map(self, **kwargs) -> DomainMethod:

        # Create the result.
        result = DomainMethod(self.to_primitive('map'))
        
        # Map the parameters
        result.parameters = [parameter.map() for parameter in self.parameters]
        
        # Return the result
        return result

class DomainModelDataMapper(DomainModel):

    attributes = t.ListType(t.ModelType(DomainModelAttributeDataMapper), default=[])
    dependencies = t.ListType(t.ModelType(DomainModelDependencyDataMapper), default=[])
    methods = t.ListType(t.ModelType(DomainMethodDataMapper), default=[])
    
    class Options():
        roles = {
            'write': blacklist('id'),
            'map': blacklist('properties', 'dependencies'),
        }
        serialize_when_none = False

    def map(self) -> DomainModel:

        # Create the result
        result = DomainModel(self.to_primitive('map'))
        
        # Map the properties, dependencies, and methods.
        result.attributes = [attribute.map() for attribute in self.attributes]
        result.dependencies = [dependency.map() for dependency in self.dependencies]
        result.methods = [method.map(parent_model_id=self.id) for method in self.methods]
        
        # Return the result.
        return result
    

class AppRepositoryImplementationDataMapper(AppRepositoryImplementation):
    '''Data mapper for AppRepositoryImplementation.
    
    '''
    
    class Options():
        roles = {
            'write': blacklist(),
            'map': blacklist(),
        }
        serialize_when_none = False

    def map(self) -> AppRepositoryImplementation:
        return AppRepositoryImplementation(self.to_primitive('map'))
    

class AppRepositoryDataMapper(AppRepository):
    '''Data mapper for AppRepository.
    
    '''

    implementations = t.ListType(t.ModelType(AppRepositoryImplementationDataMapper), default=[])

    class Options():
        roles = {
            'write': blacklist('id'),
            'map': blacklist(),
        }
        serialize_when_none = False

    def map(self) -> AppRepository:
        return AppRepository(self.to_primitive('map'))
    

class YamlDomainRepository(DomainRepository):
    '''The Domain Repository implementation for YAML data storage.
    '''

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, mapper_type: type, **data):
        return mapper_type(data, strict=False)
    
    def get_domain_model(self, id: str) -> DomainModel:
        
        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # First check the value objects
        model_data = data['domain'].get('models', {})
        if id in model_data:
            mapper = self._to_mapper(DomainModelDataMapper, id=id, **model_data.get(id))
            return mapper.map()
        
        # Otherwise return None if no domain models are found.
        return None
    
    def get_domain_models(self, type: str = None) -> List[DomainModel]:

        # Load the schema file data
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the value objects data
        model_data = data['domain'].get('models', {})

        # Return the value objects
        domain_models = [self._to_mapper(DomainModelDataMapper, id=id, **value_object).map() for id, value_object in model_data.items()]

        # Filter out type is specified
        if type is not None:
            domain_models = [domain_model for domain_model in domain_models if domain_model.type == type]

        # Return the domain models
        return domain_models

    def save_domain_model(self, domain_model: DomainModel) -> None:

        # Load the schema file data.
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the domain models data.
        domain_model_data = data['domain'].get('models', {})

        # Create a data mapper from the domain model.
        domain_model_mapper = self._to_mapper(DomainModelDataMapper, **domain_model.to_primitive())

        # Set the required value of all model properties to None if they are False.
        for attribute in domain_model_mapper.attributes:
            if attribute.required == False:
                attribute.required = None

        # Add the value object to the value objects data
        domain_model_data[domain_model.id] = domain_model_mapper.to_primitive('write')

        # Save the schema file data
        with open(self.schema_file_path, 'w') as stream:
            yaml.dump(data, stream)


    def get_repository(self, id: str) -> AppRepository:
        '''Returns the repository with the input id.

        :param id: The id of the repository to retrieve.
        :type id: str
        :return: The repository with the input id.
        :rtype: class: `domain.models.AppRepository`
        '''
        
        # Load the schema file data.
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the domain repositories data.
        repos_data = data['domain'].get('repositories', {})

        # Return the repository if it exists.
        if id in repos_data:
            return self._to_mapper(AppRepositoryDataMapper, id=id, **repos_data.get(id)).map()
        
        # Otherwise return None if repository is not found.
        return None


    def save_repository(self, repository: AppRepository):
        '''Saves the input repository.

        :param repository: The repository to save.
        :type repository: class: `domain.models.AppRepository`
        '''

        # Load the schema file data.
        import yaml
        with open(self.schema_file_path, 'r') as stream:
            data = yaml.safe_load(stream)

        # Get the domain repositories data.
        repos_data = data['domain'].get('repositories', {})

        # Create a data mapper from the repository.
        repository_mapper = self._to_mapper(AppRepositoryDataMapper, **repository.to_primitive())

        # Add the repository to the repositories data.
        repos_data[repository.id] = repository_mapper.to_primitive('write')

        # Save the schema file data.
        with open(self.schema_file_path, 'w') as stream:
            yaml.dump(data, stream)