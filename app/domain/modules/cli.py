from ..entities import *

# Module dependencies
from . import i


class CliArgument(Model):
    id = t.StringType(required=True)
    cli_subcommand_id = t.StringType(required=True)
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type = t.StringType(choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType())
    action = t.StringType()

class CliSubcommand(Model):
    id = t.StringType()
    cli_command_id = t.StringType(required=True)
    name = t.StringType(required=True)
    help = t.StringType(required=True)

class AppCommand(Model):
    id = t.StringType(required=True)
    interface_id = t.StringType(required=True)
    name = t.StringType(required=True)


class CliAppInterface(i.AppInterface):
    id = t.StringType(required=True)
    type = t.StringType(required=True, choices=['cli'])

    @staticmethod
    def create(type: str):
        interface = CliAppInterface()
        interface.type = type

        return interface