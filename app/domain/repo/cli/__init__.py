from ...entities import *
from ...modules import *

class CliInterfaceRepository():

    def add_command(self, command: cli.CliCommand) -> cli.CliCommand:
        pass

    def add_parent_argument(self, argument: cli.CliArgument) -> cli.CliArgument:
        pass

    def add_argument(self, command_key: str, argument: cli.CliArgument, subcommand_key: str = None) -> cli.CliArgument:
        pass