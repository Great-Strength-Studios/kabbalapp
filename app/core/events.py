from schematics import types as t, Model
from schematics.transforms import blacklist

from ..domains import *

class RequestEvent(Model):
    pass

class NewAppProject(RequestEvent):
    name = t.StringType(required=True)
    key = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    class Options():
        roles = {
            'app_project.map': blacklist('key')
        }

class SetDefaultAppProject(RequestEvent):
    key = t.StringType(required=True)

class SyncAppProject(RequestEvent):
    key = t.StringType(required=True)

class AddInterface(RequestEvent):
    key = t.StringType(required=True, choices=['cli', 'flask'])

class AddDomain(RequestEvent):
    name = t.StringType(required=True)
    key = t.StringType()
    aliases = t.ListType(t.StringType(), default=[])

class AddDomainImplementation(RequestEvent):
    domain_key = t.StringType(required=True)
    key = t.StringType()
    name = t.StringType(required=True)

class UpdateDomain(RequestEvent):
    key = t.StringType(required=True)
    name = t.StringType()
    aliases = t.ListType(t.StringType())

class AddDomainModel(RequestEvent):
    domain_key = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType()
    key = t.StringType()

class AddDomainRole(RequestEvent):
    domain_key = t.StringType(required=True)
    type = t.StringType(required=True, choices=d.DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class AddDomainModelProperty(RequestEvent):

    class AddMetadata(Model):
        required = t.BooleanType(default=False)
        default = t.StringType()
        choices = t.ListType(t.StringType())
        serialized_name = t.StringType()
        deserialize_from = t.ListType(t.StringType(), default=[])

    domain_key = t.StringType(required=True)
    model_key = t.StringType(required=True)
    name = t.StringType(required=True)
    key = t.StringType(required=True)
    type = t.StringType(required=True, choices=d.DOMAIN_PROPERTY_TYPES)
    metadata = t.ModelType(AddMetadata, default={})

class SyncDomain(RequestEvent):
    key = t.StringType(required=True)
    force = t.BooleanType(default=False)
