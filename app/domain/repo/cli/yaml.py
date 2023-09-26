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
        
        # Load interfaces from schema as a list.
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        # Load interfaces from schema as a list.
        interfaces = data.get('interfaces')
        interface_data = interfaces.get('cli', {})

        # Parse out commands
        command_list = []
        commands = interface_data.get('commands', {})
        for command_key, command in commands.items():
            subcommands = command.get('subcommands', {})
            for subcommand_key, subcommand in subcommands.items():
                command_list.append(self.CliCommandDataMapper(
                    **subcommand,
                    command_key=command_key,
                    subcommand_key=subcommand_key).map())

        mapper = self.CliInterfaceTypeDataMapper(
            name=interface_data.get('name', None),
            parent_arguments=interface_data.get('parent_arguments', []),
            commands=command_list
        )
        
        # Return CLI interface type
        return mapper.map()
    
    def save_interface(self, interface: CliInterfaceType) -> CliInterfaceType:
        return super().save_interface(interface)