from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    type = context.data.type

    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise APP_KEY_REQUIRED if app key is not provided.
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
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

    # Return result.
    return interface