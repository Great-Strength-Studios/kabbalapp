from schematics import types as t, Model
from schematics.transforms import blacklist

from ..domain import *

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

class AddCliCommand(RequestEvent):
    key = t.StringType()

class AddCliParentArgument(RequestEvent):
    key = t.StringType()
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
    subcommand_key = t.StringType(required=True)
    key = t.StringType()
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

class AddCliSubcommand(RequestEvent):
    command_key = t.StringType(required=True)
    key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True, deserialize_from=['help', 'description'])

class AddDomain(RequestEvent):
    name = t.StringType(required=True)
    key = t.StringType()
    aliases = t.ListType(t.StringType(), default=[])

class GetDomain(RequestEvent):
    key = t.StringType(required=True)

class AddDomainImplementation(RequestEvent):
    domain_key = t.StringType(required=True)
    key = t.StringType()
    name = t.StringType(required=True)

class SyncDomain(RequestEvent):
    domain_key = t.StringType(required=True)
    force = t.BooleanType(default=False)

class SyncDomainImplementation(RequestEvent):
    domain_key = t.StringType(required=True)
    implementation_key = t.StringType(required=True)
    force = t.BooleanType(default=False)

class UpdateDomain(RequestEvent):
    key = t.StringType(required=True)
    name = t.StringType()
    aliases = t.ListType(t.StringType())

class AddDomainModel(RequestEvent):
    domain_key = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType()
    key = t.StringType()

class ListDomainModels(RequestEvent):
    domain_key = t.StringType()

class AddDomainRole(RequestEvent):
    domain_key = t.StringType(required=True)
    type = t.StringType(required=True, choices=d.DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class AddDomainModelProperty(RequestEvent):

    domain_key = t.StringType(required=True)
    model_key = t.StringType(required=True)
    name = t.StringType(required=True)
    key = t.StringType()
    type = t.StringType(default=d.STR_TYPE, choices=d.DOMAIN_PROPERTY_TYPES)
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    serialized_name = t.StringType()
    deserialize_from = t.ListType(t.StringType(), default=[])
    description = t.StringType()

    class Options(): 
        serialize_when_none = False
        roles = {
            'domain.add_model_property': blacklist('key')
        }