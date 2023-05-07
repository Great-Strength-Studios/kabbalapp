from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

DOMAIN_ROLE_TYPES = [
    'whitelist',
    'blacklist'
]

# Types constants
STR_TYPE =  'str'
INT_TYPE = 'int'
FLOAT_TYPE = 'float'
BOOL_TYPE = 'bool'
DATETIME_TYPE = 'datetime'
DATE_TYPE = 'date'
LIST_TYPE = 'list'
DICT_TYPE = 'dict'
MODEL_TYPE = 'model'

DOMAIN_PROPERTY_TYPES = [
    STR_TYPE,
    INT_TYPE,
    FLOAT_TYPE,
    BOOL_TYPE,
    DATETIME_TYPE,
    DATE_TYPE,
    LIST_TYPE,
    DICT_TYPE,
    MODEL_TYPE
]

class AppDomainModelProperty(Model):
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(default=STR_TYPE, choices=DOMAIN_PROPERTY_TYPES)
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    serialized_name = t.StringType()
    deserialize_from = t.ListType(t.StringType(), default=[])

    class Options():
        serialize_when_none = False

class AppDomainModel(Model):
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    properties = t.DictType(t.ModelType(AppDomainModelProperty), default={})

class AppDomainRole(Model):
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class AppDomainImplementation(Model):
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    models = t.DictType(t.ModelType(AppDomainModel), default={})
    roles = t.ListType(t.ModelType(AppDomainRole), default=[])

    class Options():
        roles = {
            'create': blacklist('key', 'models', 'roles'),
            'update': blacklist('key'),
        }

class AppDomain(Model):
    key = t.StringType()
    name = t.StringType(required=True)
    aliases = t.ListType(t.StringType(), default=[])
    roles = t.ListType(t.ModelType(AppDomainRole), default=[])
    models = t.DictType(t.ModelType(AppDomainModel), default={})
    impl = t.DictType(t.ModelType(AppDomainImplementation), default={})

    class Options():
        roles = {
            'create': blacklist('key', 'roles', 'models', 'impl'),
            'update': blacklist('key'),
        }