from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    request: AddDomainRole = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get app domain service.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Add role.
    role = domain_service.add_role(**request.to_primitive())

    # Return response.
    return role