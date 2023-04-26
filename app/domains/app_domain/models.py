from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

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
    
    class Metadata(Model):
        required = t.BooleanType(default=False)
        default = t.StringType()
        choices = t.ListType(t.StringType())
        serialized_name = t.StringType()
        deserialize_from = t.ListType(t.StringType(), default=[])

        class Options():
            serialize_when_none = False
    
    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
    metadata = t.ModelType(Metadata, default=None)

class AppDomainModel(Model):
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    properties = t.DictType(t.ModelType(AppDomainModelProperty), default={})

class AppDomainRole(Model):
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class AppDomain(Model):
    key = t.StringType()
    name = t.StringType(required=True)
    aliases = t.ListType(t.StringType(), default=[])
    roles = t.ListType(t.ModelType(AppDomainRole), default=[])
    models = t.DictType(t.ModelType(AppDomainModel), default={})

    class Options():
        roles = {
            'create': whitelist('key'),
            'update': blacklist('key', 'roles', 'models'),
        }