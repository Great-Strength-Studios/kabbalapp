from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    command_key = context.data.command_key
    subcommand_key = context.data.subcommand_key
    name = context.data.name
    help = context.data.help

    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # If app key is not provided, raise exception.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get cli inteface repo.
    cli_interface_repo: CliInterfaceRepository = context.services.cli_interface_repo(app_key)

    # Get cli interface.
    interface = cli_interface_repo.get_inteface()

    # Raise interface type not found error if cli interface is not configured.
    if not interface:
        raise AppError(context.errors.INTERFACE_TYPE_NOT_FOUND.format_message('cli'))
    
    # Check to see if command exists.
    exists = interface.command_exists(command_key=command_key, subcommand_key=subcommand_key)

    # Raise command already exists error if command already exists.
    if exists:
        raise AppError(context.errors.CLI_COMMAND_ALREADY_EXISTS.format_message(command_key, subcommand_key))
    
    # Create command.
    command = CliCommand.create(
        command_key=command_key, 
        subcommand_key=subcommand_key, 
        name=name, 
        help=help)
    
    # Add command to cli interface.
    interface.add_command(command)

    # Save cli interface.
    cli_interface_repo.save_interface(interface)

    # Return added command.
    return command