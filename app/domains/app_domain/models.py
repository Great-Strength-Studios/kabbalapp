from typing import List
from schematics import types as t, Model

DOMAIN_ROLE_TYPES = [
    'whitelist',
    'blacklist'
]
DOMAIN_PROPERTY_TYPES = [
    'str',
    'int',
    'float',
    'bool',
    'datetime',
    'date',
    'time',
    'list',
    'dict',
    'model'
]

class AppDomainModelProperty(Model):
    name: t.StringType(required=True)
    type: t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
    required: t.BooleanType(default=False)
    default: t.StringType()
    choices: t.ListType(t.StringType())
    serialized_name = t.StringType()
    deserialize_from = t.ListType(t.StringType(), default=[])

class AppDomainModel(Model):
    name = t.StringType(required=True)

class AppDomainRole(Model):
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)


class AppDomain(Model):
    key = t.StringType()
    name = t.StringType(required=True)
    roles = t.ListType(t.ModelType(AppDomainRole), default=[])
    models = t.DictType(t.ModelType(AppDomainModel), default={})