from typing import List
from schematics import types as t, Model
from schematics.transforms import whitelist, blacklist
from schematics.types.serializable import serializable

class AppArgument(Model):
    key = t.StringType(required=True)
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type = t.StringType(default='str', choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType())
    action = t.StringType()

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_argument': blacklist('key'),
            'cli.add_parent_argument': blacklist('key'),
        }

class AppSubcommand(Model):
    name = t.StringType(required=True)
    help = t.StringType(required=True)
    arguments = t.DictType(t.ModelType(AppArgument), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_subcommand': blacklist('arguments')
        }

class AppCommand(Model):
    key = t.StringType(required=True)
    subcommands = t.DictType(t.ModelType(AppSubcommand), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_command': blacklist('key', 'commands', 'parent_arguments')
        }

class AppCommands(Model):
    parent_arguments = t.DictType(t.ModelType(AppArgument), default={})
    commands = t.DictType(t.ModelType(AppCommand), default={})