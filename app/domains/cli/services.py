from .models import *

class CliInterfaceService():

    def add_command(self, key: str) -> AppCommand:
        pass

    def add_parent_argument(self, key: str, name_or_flags: List[str], help: str, **kwargs) -> AppArgument:
        pass