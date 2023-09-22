from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

from ...constants import *

class AppDomainModelProperty(Model):
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(default=STR_TYPE, choices=DOMAIN_PROPERTY_TYPES)
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    serialized_name = t.StringType()
    deserialize_from = t.ListType(t.StringType(), default=[])
    description = t.StringType()

    class Options():
        serialize_when_none = False
        roles = {
            'domain.add_property': blacklist('key'),
        }

class AppDomainModel(Model):
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    properties = t.DictType(t.ModelType(AppDomainModelProperty), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'domain.add_model': blacklist('key', 'properties'),
            'domain.add_property': blacklist('key'),
            'domain.get_domain': blacklist('properties'),
            'domain.list_domain_models': blacklist('properties'),
        }

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
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    aliases = t.ListType(t.StringType(), default=[])
    roles = t.ListType(t.ModelType(AppDomainRole), default=[])
    models = t.DictType(t.ModelType(AppDomainModel), default={})
    impl = t.DictType(t.ModelType(AppDomainImplementation), default={})

    class Options():
        roles = {
            'create': blacklist('key', 'roles', 'models', 'impl'),
            'update': blacklist('key'),
            'domain.list_domains': blacklist('roles', 'models', 'impl', 'aliases'),
            'domain.get_domain': blacklist(),
        }