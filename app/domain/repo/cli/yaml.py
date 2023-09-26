from app.domain.modules import CliInterfaceType
from . import *

class YamlRepository(CliInterfaceRepository):

    class CliInterfaceTypeDataMapper(CliInterfaceType):

        class Options():
            roles = {
                'write': blacklist('commands')
            }
        
        def map(self):
            return CliInterfaceType(self.to_primitive())

    class CliCommandDataMapper(CliCommand):

        class Options():
            roles = {
                'write': blacklist('command_key', 'subcommand_key'),
            }

        def map(self):
            return CliCommand(self.to_primitive())

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)

    def get_inteface(self) -> CliInterfaceType:
        return super().get_inteface()
    
    def save_interface(self, interface: CliInterfaceType) -> CliInterfaceType:
        return super().save_interface(interface)