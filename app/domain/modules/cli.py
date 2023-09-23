from ..entities import *

# Module dependencies
from . import i


class CliArgument(Model):
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type = t.StringType(choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType())
    action = t.StringType()

class CliCommand(Model):
    command_key = t.StringType(required=True)
    subcommand_key = t.StringType()
    name = t.StringType(required=True)
    help = t.StringType(required=True)
    arguments = t.ListType(t.ModelType(CliArgument), default=[])

    @staticmethod
    def create(command_key: str, name: str, help: str, subcommand_key: str = None, arguments: List[CliArgument] = []):
        command = CliCommand()
        command.command_key = command_key
        command.name = name
        command.help = help
        command.subcommand_key = subcommand_key
        command.arguments = arguments

        return command


class CliInterfaceType(i.AppInterfaceType):
    mappers = t.DictType(t.StringType())
    commands = t.ListType(t.ModelType(CliCommand), default=[])

    @staticmethod
    def create(type: str):
        interface = CliInterfaceType()
        interface.type = type

        return interface