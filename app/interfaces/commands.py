from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

class RequestEvent(Model):
    pass

class NewAppProject(RequestEvent):
    name = t.StringType(required=True)
    tag = t.StringType(required=True)
    app_directory = t.StringType(required=True)

class SetDefaultAppProject(RequestEvent):
    tag = t.StringType(required=True)

class AddInterface(RequestEvent):
    name = t.StringType(required=True)
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

class AddDomainModel(RequestEvent):
    name = t.StringType(required=True)
    type = t.StringType(required=True)
    class_name = t.StringType()
    base_type_model_id = t.StringType()

class AddDomainModelProperty(RequestEvent):
    model_id = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(default='str')
    inner_type = t.StringType()
    inner_type_model_id = t.StringType()
    poly_type_model_ids = t.ListType(t.StringType())
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    description = t.StringType()
    type_properties = t.DictType(t.StringType(), default={})

class PrintDomainModelModule(RequestEvent):
    pass
