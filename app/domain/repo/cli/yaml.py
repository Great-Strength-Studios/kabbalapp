from app.domain.modules import CliInterfaceType
from . import *

class CliCommandDataMapper(CliCommand):

    class Options():
        roles = {
            'write': blacklist('command_key', 'subcommand_key'),
        }

    def map(self):
        return CliCommand(self.to_primitive())
    
    @staticmethod
    def to_mapper(**data) -> 'CliCommandDataMapper':
        return CliCommandDataMapper(data, strict=False)

class CliInterfaceTypeDataMapper(CliInterfaceType):

    commands = t.ListType(t.ModelType(CliCommandDataMapper), default=[])
    class Options():
        roles = {
            'write': blacklist('commands')
        }

    def map(self):
        return CliInterfaceType(self.to_primitive())
    
    @staticmethod
    def to_mapper(**data) -> 'CliInterfaceTypeDataMapper':
        return CliInterfaceTypeDataMapper(data, strict=False)

class YamlRepository(CliInterfaceRepository):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)
    
    def _to_mapper(self, type: type, **data):
        return type(data, strict=False)

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
                command_list.append(self.to_mapper(
                    CliCommandDataMapper,
                    **subcommand,
                    command_key=command_key,
                    subcommand_key=subcommand_key))

        mapper = self.CliInterfaceTypeDataMapper(
            name=interface_data.get('name', None),
            parent_arguments=interface_data.get('parent_arguments', []),
            commands=command_list
        )
        
        # Return CLI interface type
        return mapper.map()
    
    def save_interface(self, interface: CliInterfaceType) -> CliInterfaceType:
            
            # Load interfaces from schema as a list.
            import yaml
            with open(self.schema_file_path, 'r') as f:
                data = yaml.safe_load(f)
            
            # Load interfaces from schema as a list.
            interfaces = data.get('interfaces', {})
            
            # Add new interface
            mapper = self._to_mapper(
                CliInterfaceTypeDataMapper,
                **interface.to_primitive())
            interfaces['cli'] = mapper.to_primitive('write')

            # Add commands to interface.
            for command in mapper.commands:
                command_data = self._to_mapper(
                    CliCommandDataMapper,
                    **command.to_primitive()).to_primitive('write')
                if not command.subcommand_key:
                    interfaces['cli']['commands'][command.command_key] = command_data
                else:
                    interfaces['cli']['commands'][command.command_key]['subcommands'][command.subcommand_key] = command_data
    
            # Update the interfaces in the schema.
            data['interfaces'] = interfaces
    
            # Write the schema back to the file.
            with open(self.schema_file_path, 'w') as f:
                yaml.dump(data, f)
    
            return interface