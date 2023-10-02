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


class DateTimeTypeProperties(TypeProperties):

	formats = t.StringType()
	serialized_format = t.StringType()
	parser = t.StringType()
	tzd = t.StringType(default='allow', choices=['require', 'allow', 'utc', 'reject'])
	convert_tz = t.BooleanType(default=False)
	drop_tzinfo = t.BooleanType(default=False)

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


class DomainModelProperty(ValueObject):
	
	name = t.StringType(required=True)
	type = t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
	inner_type = t.StringType()
	required = t.BooleanType()
	default = t.StringType()
	choices = t.ListType(t.StringType())
	description = t.StringType()
	type_properties = t.ModelType(TypeProperties)

	@staticmethod
	def create(name: str, type: str = 'str', inner_type: str = None, required: bool = False, default: str = None, choices: List[str] = [], description: str = None, type_properties: TypeProperties = None) -> 'DomainModelProperty':
		result = DomainModelProperty()
		result.name = name
		result.type = type
		result.inner_type = inner_type
		result.required = required
		result.default = default
		result.choices = choices
		result.description = description
		result.type_properties = type_properties

		result.validate()

		return result

class AppValueObject(Entity):
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    properties = t.ListType(t.ModelType(DomainModelProperty), default=[])

    @staticmethod
    def create(name: str, class_name: str, id: str = None, properties: List[DomainModelProperty] = []) -> 'AppValueObject':
        result = AppValueObject()
        result.name = name
        result.class_name = class_name
        result.properties = properties

        # Convert python camel case to snake case if ID is not provided
        if id is None:
            import re
            result.id = name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        else:
            result.id = id

        result.validate()

        return result
    
    def has_property(self, property: DomainModelProperty) -> bool:
        return any((p.name == property.name for p in self.properties))

    def add_property(self, property: DomainModelProperty) -> None:
        self.properties.append(property)