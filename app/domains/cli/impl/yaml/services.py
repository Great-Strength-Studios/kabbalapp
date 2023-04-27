from .models import *
from ...services import *

class YamlCliInterfaceService(CliInterfaceService):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    @property
    def schema_file_path(self) -> str:
        import os
        return os.path.join(self.app_directory, self.schema_location)

    def add_command(self, key: str) -> AppCommand:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        command = AppCommand({'key': key})
        command_data = command.to_primitive('cli.add_command')
        cli_interface_data = data['interfaces']['cli']
        try:
            if cli_interface_data['commands'] is not None and key in cli_interface_data['commands']:
                return ('CLI_COMMAND_ALREADY_EXISTS', key)
            if cli_interface_data['commands'] is None:
                cli_interface_data['commands'] = {key: command_data}
            else:
                cli_interface_data['commands'][key] = command_data
        except KeyError:
            cli_interface_data['commands'] = {key: command_data}
        data['interfaces']['cli'] = cli_interface_data
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        return command
    
    def add_parent_argument(self, key: str, name_or_flags: str, help: str, **kwargs) -> AppArgument:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        argument = AppArgument({'key': key, 'name_or_flags': name_or_flags, 'help': help, **kwargs})
        commands = AppCommands(data['interfaces']['cli'])
        if key in commands.parent_arguments:
            return ('CLI_ARGUMENT_ALREADY_EXISTS', key)
        commands.parent_arguments[key] = argument.to_primitive('cli.add_parent_argument')
        data['interfaces']['cli'] = commands.to_primitive()
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        return argument
    
    def add_subcommand(self, command_key: str, key: str, name: str, help: str) -> AppSubcommand:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        subcommand = AppSubcommand({'key': key, 'name': name, 'help': help})
        commands = AppCommands(data['interfaces']['cli'])
        try:
            command = commands.commands[command_key]
        except KeyError:
            return ('CLI_COMMAND_NOT_FOUND', command_key)
        if key in command.subcommands:
            return ('CLI_SUBCOMMAND_ALREADY_EXISTS', key)
        command.subcommands[key] = subcommand.to_primitive('cli.add_subcommand')
        data['interfaces']['cli'] = commands.to_primitive()
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        return subcommand
    
    def add_argument(self, command_key: str, subcommand_key: str, key: str, name_or_flags: str, help: str, **kwargs) -> AppArgument:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        argument = AppArgument({'key': key, 'name_or_flags': name_or_flags, 'help': help, **kwargs})
        commands = AppCommands(data['interfaces']['cli'])
        try:
            command = commands.commands[command_key]
        except KeyError:
            return ('CLI_COMMAND_NOT_FOUND', command_key)
        try:
            subcommand = command.subcommands[subcommand_key]
        except KeyError:
            return ('CLI_SUBCOMMAND_NOT_FOUND', subcommand_key)
        if key in subcommand.arguments:
            return ('CLI_ARGUMENT_ALREADY_EXISTS', key)
        subcommand.arguments[key] = argument.to_primitive('cli.add_argument')
        data['interfaces']['cli'] = commands.to_primitive()
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        return argument
        