from ...core import *
from ...domain import *


CLI_MAPPERS_CONTENT = """from .command import *
from .header import *"""

CLI_COMMAND_MAPPER_CONTENT = """from ..commands import *
"""

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
            'mappers/header.py': ''
        }

        # For each file in cli_files, create a new block and append it to the block list
        for file, content in cli_files.items():
            blocks.append(target_app_printer.new_block('app/interfaces/cli', file, content))
        
        # Print blocks to target app printer.
        for block in blocks:
            if not target_app_printer.block_exists(block.file_path):
                target_app_printer.print_block(block)


    def save_interface_config():
    
        # Get interface service.
        interface_repo: AppInterfaceRepository = context.services.interface_repo(app_key)

        # Raise INTERFACE_ALREADY_EXISTS if interface already exists.
        if interface_repo.get_interface(type):
            raise AppError(context.errors.INTERFACE_ALREADY_EXISTS.format_message(type))

        # If the input interface type is 'cli', then create a new CliAppInterface instance.
        if type == 'cli':
            interface = cli.CliAppInterface.create(type)
        else:
            raise AppError(context.errors.INVALID_INTERFACE_TYPE)

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