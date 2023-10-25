from ..core.domain import *
from .constants import *


class TypeProperties(ValueObject):
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
    
class ModelProperty(ValueObject):

    name = t.StringType(required=True)
    type = t.StringType(required=True)
    inner_type = t.StringType()
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType)
    description = t.StringType()
    type_properties = t.PolyModelType([StringTypeProperties, DateTypeProperties, DateTimeTypeProperties, ListTypeProperties, DictTypeProperties])

    def update(self):

        # If the setting is "required", cast the value to a boolean and set to the required attribute


        # If the setting is "choices", assume that any non-null value is a string containing a comma-separated list. 
        # Split the list by ",", strip out any white spaces, and set to the choices attribute.


        # Otherwise, set the passed in value to the attribute.
        pass

