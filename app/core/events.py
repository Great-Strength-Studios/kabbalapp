from schematics import types as t, Model
from schematics.transforms import blacklist

from ..constants import *

class RequestEvent(Model):
    pass

class NewAppProject(RequestEvent):
    name = t.StringType(required=True)
    app_key = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    class Options():
        roles = {
            'app_project.map': blacklist('app_key')
        }

class SyncAppProject(RequestEvent):
    app_key = t.StringType(required=True)

class AddDomain(RequestEvent):
    name = t.StringType(required=True)
    key = t.StringType()

class AddDomainModel(RequestEvent):
    domain_key = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType()
    key = t.StringType()

class AddDomainRole(RequestEvent):
    domain_key = t.StringType(required=True)
    key = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)