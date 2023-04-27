from typing import List
from schematics import types as t, Model
from schematics.transforms import whitelist, blacklist
from schematics.types.serializable import serializable

class AppArgument(Model):
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type = t.StringType(default='str', choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType())
    action = t.StringType()

class AppSubcommand(Model):
    help = t.StringType(required=True)
    arguments = t.ListType(t.ModelType(AppArgument), default=[])

    class Options():
        serialize_when_none = False
        roles = {
            'add_subparser': blacklist('arguments')
        }

class AppCommand(Model):
    key = t.StringType(required=True)
    subcommands = t.DictType(t.ModelType(AppSubcommand), default=[])

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_command': blacklist('key', 'commands', 'parent_arguments')
        }

class AppCommands(Model):
    parent_arguments = t.ListType(t.ModelType(AppArgument), default=[])
    commands = t.DictType(t.ModelType(AppCommand), default={})