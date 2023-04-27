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