from .models import *

class CliInterfaceService():

    def add_command(self, key: str) -> AppCommand:
        pass

    def add_parent_argument(self, key: str, name_or_flags: List[str], help: str, **kwargs) -> AppArgument:
        pass

    def add_subcommand(self, command_key: str, key: str, name: str, help: str) -> AppSubcommand:
        pass

    def add_argument(self, command_key: str, subcommand_key: str, key: str, name_or_flags: List[str], help: str, **kwargs) -> AppArgument:
        pass