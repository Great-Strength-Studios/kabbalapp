from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    request = context.data

    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise APP_KEY_REQUIRED if app key is not provided.
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get interface service.
    interface_service = context.services.interface_service(app_key)

    # Add interface.
    interface_service.add_interface(**request.to_primitive())