from ..entities import *

# Dependencies
from . import i

class CliAppInterface(i.AppInterface):
    type = t.StringType(required=True, choices=['cli'])
    cli_commands = t.DictType(t.StringType())

    @staticmethod
    def create(type: str, cli_commands: dict):
        interface = CliAppInterface()
        interface.type = type
        interface.cli_commands = cli_commands

        return interface