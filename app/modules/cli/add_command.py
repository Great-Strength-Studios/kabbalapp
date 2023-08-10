from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    request: AddCliCommand = context.data

    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # If app key is not provided, raise exception.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get cli inteface service.
    service: cli.CliInterfaceService = context.services.cli_interface_service(app_key)

    # Add command to cli interface.
    command = service.add_command(**request.to_primitive())

    # If cli command already exists, raise exception.
    if isinstance(command, tuple):
        raise AppError(context.errors.get(command[0]).format_message(*command[1:]))
    
    # Return cli command.
    return command