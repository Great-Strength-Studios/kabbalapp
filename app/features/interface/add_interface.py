from ...core import *
from ...domain import *


CLI_MAPPERS_CONTENT = """from .command import *
from .header import *"""

CLI_COMMAND_MAPPER_CONTENT = """from ...commands import *
"""

CLI_HEADER_MAPPER_CONTENT = """def default(request, app_context, **kwargs):
    return {}"""

def handle(context: MessageContext):

    # Unpack request.
    type = context.data.type

    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise APP_KEY_REQUIRED if app key is not provided.
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    def copy_cli_interface_files():

        # Load local app printer.
        app_printer: AppPrinter = context.services.app_printer()

        # Load target app printer.
        target_app_printer: AppPrinter = context.services.app_printer(app_key)

        # List cli files to copy.
        cli_files = [
            '__init__.py',
            'arguments.py',
            'config.py'
        ]

        # Read blocks for cli file from current app printer
        blocks = [app_printer.read_block(file, base_path='app/interfaces/cli') for file in cli_files]

        # List cli files to write.
        cli_files = {
            'mappers/__init__.py': CLI_MAPPERS_CONTENT,
            'mappers/command.py': CLI_COMMAND_MAPPER_CONTENT,
            'mappers/header.py': CLI_HEADER_MAPPER_CONTENT
        }

        # For each file in cli_files, create a new block and append it to the block list
        for file, content in cli_files.items():
            blocks.append(target_app_printer.new_block('app/interfaces/cli', file, content))
        
        # Print blocks to target app printer.
        for block in blocks:
            if not target_app_printer.block_exists(block.file_path):
                target_app_printer.print_block(block)

        # Make updates to interface package file.
        interface_package_file = target_app_printer.read_block('app/interfaces/__init__.py')

        # Add cli interface import to interface package file.
        if len(interface_package_file.code_lines) == 1:
            interface_package_file.add_line('')
        
        interface_package_file.add_line('from .cli import CliAppBuilder, CliAppContext, arguments as args')
        target_app_printer.print_block(interface_package_file)


    def save_interface_config():
    
        # Get interface service.
        app_interface_repo: i.AppInterfaceRepository = context.services.interface_repo(app_key)

        # Raise INTERFACE_ALREADY_EXISTS if interface already exists.
        interfaces = app_interface_repo.get_interfaces()
        if type in [interface.type for interface in interfaces]:
            raise AppError(context.errors.INTERFACE_ALREADY_EXISTS.format_message(type))

        # If the input interface type is 'cli', then create a new CliAppInterface instance and replace the interface repo instance
        if type == 'cli':
            interface_repo: cli.CliInterfaceRepository = context.services.cli_interface_repo(app_key)
            interface = cli.CliInterfaceType.create(type)
        else:
            raise AppError(context.errors.INTERFACE_TYPE_NOT_FOUND)

        # Add interface.
        interface_repo.save_interface(interface)

        return interface

    # It type is 'cli', then copy cli files.
    if type == 'cli':
        copy_cli_interface_files()

    # Save interface config.
    interface = save_interface_config()

    # Return result.
    return interface