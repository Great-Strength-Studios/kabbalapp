from ..entities import *

# Module dependencies
from .interface import AppInterfaceType


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

class CliInterfaceType(AppInterfaceType):
    mappers = t.DictType(t.StringType())
    commands = t.ListType(t.ModelType(CliCommand), default=[])
    parent_arguments = t.ListType(t.ModelType(CliArgument), default=[])

    @staticmethod
    def create(type: str):
        interface = CliInterfaceType()
        interface.type = type

        return interface
    
    def command_exists(self, command_key: str, subcommand_key: str = None):
        return any([command for command in self.commands if command.command_key == command_key and command.subcommand_key == subcommand_key])
    
    def add_command(self, command: CliCommand):
        self.commands.append(command)

    def parent_argument_exists(self, flags: List[str]):
        for flag in flags:
            if any([argument for argument in self.parent_arguments if flag in argument.name_or_flags]):
                return True
        return False
    
    def add_parent_argument(self, argument: CliArgument):
        self.parent_arguments.append(argument)