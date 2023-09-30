from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

from ..constants import *


class TypeProperties(Model):
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


class DomainModelProperty(Model):
	
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