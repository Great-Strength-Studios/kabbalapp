from ..entities import *

# Module dependencies
from . import i


class CliArgument(Model):
    key = t.StringType(required=True)
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type = t.StringType(choices=['str', 'int', 'float'])
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

class CliSubcommand(Model):
    key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True)
    arguments = t.DictType(t.ModelType(CliArgument), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_subcommand': blacklist('key', 'arguments')
        }

class AppCommand(Model):
    key = t.StringType(required=True)
    subcommands = t.DictType(t.ModelType(CliSubcommand), default={})

    class Options():
        serialize_when_none = False
        roles = {
            'cli.add_command': blacklist('key', 'commands', 'parent_arguments')
        }

class AppCommands(Model):
    parent_arguments = t.DictType(t.ModelType(CliArgument), default={})
    commands = t.DictType(t.ModelType(AppCommand), default={})


class CliAppInterface(i.AppInterface):
    type = t.StringType(required=True, choices=['cli'])
    cli_commands = t.DictType(t.StringType())

    @staticmethod
    def create(type: str, cli_commands: dict = None):
        interface = CliAppInterface()
        interface.type = type
        interface.cli_commands = cli_commands

        return interface