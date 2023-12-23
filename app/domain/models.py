from ..core.domain import *
from .constants import *


class TypeProperties(AppValueObject):
    pass


class StringTypeProperties(TypeProperties):

    regex = t.StringType()
    min_length = t.IntType()
    max_length = t.IntType()

    @staticmethod
    def create(regex: str = None, min_length: int = None, max_length: int = None) -> 'StringTypeProperties':
        result = StringTypeProperties()
        result.regex = regex
        if min_length is not None:
            result.min_length = int(min_length)
        if max_length is not None:
            result.max_length = int(max_length)

        result.validate()

        return result


class DateTypeProperties(TypeProperties):
    
    formats = t.StringType()

    @staticmethod
    def create(formats: str = None) -> 'DateTypeProperties':
        result = DateTypeProperties()
        result.formats = formats

        result.validate()

        return result


class DictTypeProperties(TypeProperties):

    coerce_key = t.StringType()

    @staticmethod
    def create(coerce_key: str = None) -> 'DictTypeProperties':
        result = DictTypeProperties()
        result.coerce_key = coerce_key

        result.validate()

        return result


class DateTimeTypeProperties(TypeProperties):

    formats = t.StringType()
    serialized_format = t.StringType()
    parser = t.StringType()
    tzd = t.StringType(default='allow', choices=['require', 'allow', 'utc', 'reject'])
    convert_tz = t.BooleanType(default=False)
    drop_tzinfo = t.BooleanType(default=False)

    @staticmethod
    def create(formats: str = None, serialized_format: str = None, parser: str = None, tzd: str = None, convert_tz: bool = None, drop_tzinfo: bool = None) -> 'DateTimeTypeProperties':
        result = DateTimeTypeProperties()
        result.formats = formats
        result.serialized_format = serialized_format
        result.parser = parser
        result.tzd = tzd
        result.convert_tz = convert_tz
        result.drop_tzinfo = drop_tzinfo

        result.validate()

        return result

class ListTypeProperties(TypeProperties):

    min_size = t.IntType()
    max_size = t.IntType()

    @staticmethod
    def create(min_size: int = None, max_size: int = None) -> 'ListTypeProperties':
        result = ListTypeProperties()
        if min_size is not None:
            result.min_size = int(min_size)
        if max_size is not None:
            result.max_size = int(max_size)

        result.validate()

        return result
    
class Attribute(AppValueObject):

    type = t.StringType(required=True, choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'list', 'dict', 'model', 'poly'])
    inner_type = t.StringType()
    inner_type_model_id = t.StringType()
    poly_type_model_ids = t.ListType(t.StringType())
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType)
    type_properties = t.PolyModelType([StringTypeProperties, DateTypeProperties, DateTimeTypeProperties, ListTypeProperties, DictTypeProperties])

    def update(self, setting: str, value: str = None):

        # If the setting is "required", cast the value to a boolean and set to the required attribute
        if setting == 'required':
            self.required = bool(value)

        # If the setting is "choices", assume that any non-null value is a string containing a comma-separated list. 
        # Split the list by ",", strip out any white spaces, and set to the choices attribute.
        # Otherwise set the choices attribute to None.
        elif setting == 'choices':
            if value is not None:
                self.choices = [choice.strip() for choice in value.split(',')]
            else:
                self.choices = None

        # Otherwise, set the passed in value to the attribute.
        else:
            setattr(self, setting, value)


class Parameter(AppValueObject):

    type = t.StringType(required=True, choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'list', 'dict', 'model'])
    inner_type = t.StringType()
    type_model_id = t.StringType()
    required = t.BooleanType()
    default = t.StringType()


class Method(AppValueObject):

    method_name = t.StringType(required=True)
    return_type = t.StringType(choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'list', 'dict', 'model'])
    inner_return_type = t.StringType(choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'model'])
    return_type_model_id = t.StringType()
    parameters = t.ListType(t.ModelType(Parameter), default=[])

    def add_parameter(self, parameter: Parameter):
        '''
        Adds the input parameter to the list of method parameters.
        
        :param parameter: The parameter to add to the method.
        :type parameter: `domain.models.Parameter`
        '''

        # Add the parameter to the parameters list.
        self.parameters.append(parameter)


class DomainMethodParameter(Parameter):
    
    @staticmethod
    def create(name: str, type: str, inner_type: str = None, inner_type_model_id: str = None, required: bool = None, default: str = None, description: str = None) -> 'DomainMethodParameter':

        # Create new model instance.
        result = DomainMethodParameter()

        # Load attributes from passed in values.
        result.name = name
        result.type = type
        result.description = description
        result.inner_type = inner_type
        result.type_model_id = inner_type_model_id
        result.required = required
        result.default = default

        # Validate model instance.
        result.validate()

        # Return model instance.
        return result

class DomainMethod(AppValueObject):
    
    type = t.StringType(required=True, choices=['factory', 'behavior'])
    return_type = t.StringType(choices=['str', 'int', 'float', 'bool', 'date', 'datetime', 'model'])
    inner_return_type = t.StringType()
    parameters = t.ListType(t.ModelType(DomainMethodParameter), default=[])

    @staticmethod
    def create(name: str, type: str, description: str, return_type: str = None, inner_return_type: str = None) -> 'DomainMethod':

        # Create new model instance.
        result = DomainMethod()

        # Load attributes from passed in values.
        result.name = name
        result.type = type
        result.description = description
        result.return_type = return_type
        result.inner_return_type = inner_return_type

        # Validate model instance.
        result.validate()

        # Return model instance.
        return result
    
    def has_parameter(self, parameter: DomainMethodParameter) -> bool:
        '''Returns True if a parameter with the same name as the input parameter exists in the domain method parameters list.
        
        :param parameter: The parameter to check if it already exists in the method.
        :type parameter: `domain.models.DomainMethodParameter`
        :returns: True if the parameter already exists in the method, otherwise False.
        :rtype: bool
        '''

        # Check to see if any existing parameter has a name matching the input parameter name.
        return any([p.name == parameter.name for p in self.parameters])
    
    def add_parameter(self, parameter: DomainMethodParameter):
        '''Adds the input parameter to the domain method parameters list.
        
        :param parameter: The parameter to add to the method.
        :type parameter: `domain.models.DomainMethodParameter`
        '''

        # Add the parameter to the parameters list.
        self.parameters.append(parameter)
    

class AppRepositoryImplementation(AppValueObject):
    '''An implementation of an AppRepository for a particular data storage type.

    '''

    class_name = t.StringType(required=True)

    @staticmethod
    def create(name: str, class_name: str, description: str) -> 'AppRepositoryImplementation':

        # Create new model instance.
        result = AppRepositoryImplementation()

        # Load attributes from passed in values.
        result.class_name = class_name
        result.description = description

        # Update name to be lower cased and underscored.
        result.name = name.lower().replace(' ', '_')

        # Validate model instance.
        result.validate()

        # Return model instance.
        return result


class AppRepository(AppEntity):
    '''A repository interface used to store and retrieve domain models.
    '''

    class_name = t.StringType(required=True)
    implementations = t.ListType(t.ModelType(AppRepositoryImplementation), default=[])

    @staticmethod
    def create(name: str, class_name: str, description: str) -> 'AppRepository':
        '''Creates a new AppRepository instance.
        
        :param name: The name of the repository.
        :type name: str
        :param class_name: The class name of the repository.
        :type class_name: str
        :param description: The description of the repository for inline documentation.
        :type description: str
        :returns: A new AppRepository instance.
        :rtype: `domain.models.AppRepository`
        '''
        # Create new model instance.
        result = AppRepository()

        # Load attributes from passed in values.
        result.name = name
        result.class_name = class_name
        result.description = description

        # Set id as the lower cased and underscored name.
        result.id = name.lower().replace(' ', '_')

        # Validate model instance.
        result.validate()

        # Return model instance.
        return result
    
    def has_implementation(self, implementation_name: str) -> bool:
        '''Returns True if the input implementation already exists in the repository implementations list.
        
        :param implementation_name: The name of the implementation to check if it already exists in the repository.
        :type implementation: `str`
        :returns: True if the implementation already exists in the repository, otherwise False.
        :rtype: bool
        '''

        # Check to see if any existing implementation has a name matching the input implementation name.
        return any([i.name == implementation_name for i in self.implementations])
    
    def add_implementation(self, implementation: AppRepositoryImplementation):
        '''Adds the input implementation to the repository implementations list.
        
        :param implementation: The implementation to add to the repository.
        :type implementation: `domain.models.AppRepositoryImplementation`
        '''

        # Add the implementation to the implementations list.
        self.implementations.append(implementation)