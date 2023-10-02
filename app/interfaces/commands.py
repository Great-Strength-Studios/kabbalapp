from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

from ..constants import *

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

class AddInterface(RequestEvent):
    type = t.StringType(required=True, choices=['cli', 'rest_flask'])

class AddCliCommand(RequestEvent):
    command_key = t.StringType(required=True)
    subcommand_key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])

class AddCliParentArgument(RequestEvent):
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])
    type = t.StringType(choices=['str', 'int', 'float'])
    flags = t.ListType(t.StringType(), default=[])
    positional = t.BooleanType(default=False)
    default = t.StringType()
    required = t.BooleanType()
    choices = t.ListType(t.StringType(), default=[])
    nargs = t.StringType()
    action = t.StringType()

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_parent_argument': blacklist('name', 'flags', 'positional'),
        }

class AddCliArgument(RequestEvent):
    command_key = t.StringType(required=True)
    subcommand_key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])
    type = t.StringType(choices=['str', 'int', 'float'])
    flags = t.ListType(t.StringType(), default=[])
    positional = t.BooleanType(default=False)
    default = t.StringType()
    required = t.BooleanType()
    choices = t.ListType(t.StringType(), default=[])
    nargs = t.StringType()
    action = t.StringType()

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_argument': blacklist('name', 'flags', 'positional'),
        }

class AddDomainImplementation(RequestEvent):
    domain_key = t.StringType(required=True)
    key = t.StringType()
    name = t.StringType(required=True)

class SyncDomainImplementation(RequestEvent):
    domain_key = t.StringType(required=True)
    implementation_key = t.StringType(required=True)
    force = t.BooleanType(default=False)

class AddDomainModel(RequestEvent):
    name = t.StringType(required=True)
    type = t.StringType(required=True)
    class_name = t.StringType()

class ListDomainModels(RequestEvent):
    domain_key = t.StringType()

class AddDomainRole(RequestEvent):
    domain_key = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class AddDomainModelProperty(RequestEvent):
    model_id = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(default=STR_TYPE, choices=DOMAIN_PROPERTY_TYPES)
    inner_type = t.StringType()
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    description = t.StringType()
    type_properties = t.DictType(t.StringType(), default={})

class PrintValueObjectModule(RequestEvent):
    pass
