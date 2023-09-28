from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

from ..constants import *


class ModelProperty(Model):
	
	name = t.StringType(required=True)
	type = t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
	required = t.BooleanType()
	default = t.StringType()
	choices = t.ListType(t.StringType())
	description = t.StringType()

	@staticmethod
	def create(name: str, type: str = 'str', required: bool = False, default: str = None, choices: List[str] = [], description: str = None) -> 'ModelProperty':
		result = ModelProperty()
		result.name = name
		result.type = type
		result.required = required
		result.default = default
		result.choices = choices
		result.description = description

		return result