from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

class AppArgumentConfiguration(Model):
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type_str = t.StringType(default='str', choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType())
    action = t.StringType()

    @serializable
    def type(self):
        if self.action in ['store_true', 'store_false']:
            return None
        if self.type_str == 'str':
            return str
        elif self.type_str == 'int':
            return int
        elif self.type_str == 'float':
            return float
        else:
            raise Exception('Invalid type')
    
    class Options():
        serialize_when_none = False
        roles = {
            'add_argument': blacklist('type_str', 'name_or_flags')
        }

class AppSubcommandConfiguration(Model):
    name = t.StringType(required=True)
    help = t.StringType(required=True)
    arguments = t.DictType(t.ModelType(AppArgumentConfiguration), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'add_subparser': blacklist('arguments')
        }

class AppCommandConfiguration(Model):
    help = t.StringType(required=True)
    cli_subcommands = t.DictType(t.ModelType(AppSubcommandConfiguration), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'add_parser': blacklist('cli_subcommands')
        }

class AppCommandsConfiguration(Model):
    type = t.StringType(required=True)
    parent_arguments = t.DictType(t.ModelType(AppArgumentConfiguration), default={})
    mappers = t.DictType(t.StringType())
    cli_commands = t.DictType(t.ModelType(AppCommandConfiguration), default={})