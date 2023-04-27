from .models import *
from ...services import *

class YamlCliInterfaceService(CliInterfaceService):

    def __init__(self, app_directory: str, schema_location: str):
        self.app_directory = app_directory
        self.schema_location = schema_location

    def add_command(self, key: str) -> AppCommand:
        import yaml
        with open(self.schema_file_path, 'r') as f:
            data = yaml.safe_load(f)
        command = AppCommand(key)
        command_data = command.to_primitive('cli.add_command')
        try:
            if data['commands'] is not None and key in data['commands']:
                return ('COMMAND_ALREADY_EXISTS', key)
            if data['commands'] is None:
                data['commands'] = {key: command_data}
            else:
                data['commands'][key] = command_data
        except KeyError:
            data['commands'] = {key: command_data}
        with open(self.schema_file_path, 'w') as f:
            yaml.dump(data, f)
        raw_data = {
            'key': key
        }
        return AppCommand(raw_data=raw_data)