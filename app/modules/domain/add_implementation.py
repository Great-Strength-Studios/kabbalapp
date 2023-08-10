from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    request = context.data

    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # If app key is not provided, raise exception.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain service.
    service: d.AppDomainService = context.services.domain_service(app_key)

    # If key is not provided, generate one from name.
    if not request.key:
        request.key = request.name.lower().replace(' ', '_')

    # Add implementation to domain.
    implementation = service.add_implementation(**request.to_primitive())

    # If domain implementation already exists, raise exception.
    if isinstance(implementation, tuple):
        raise AppError(context.errors.get(implementation[0]).format_message(*implementation[1:]))
    
    # Return domain implementation.
    return implementation