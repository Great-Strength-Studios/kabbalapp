from ..entities import *

# Module dependencies
from . import i


class CliArgument(Model):
    id = t.StringType(required=True)
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


class CliInterface(i.AppInterface):
    type = t.StringType(required=True, choices=['cli'])

    @staticmethod
    def create(type: str):
        interface = CliInterface()
        interface.type = type

        return interface