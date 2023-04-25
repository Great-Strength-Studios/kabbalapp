from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Unpack request.
    request: AddDomainModelProperty = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get app domain service.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Add property.
    property = domain_service.add_property(**request.to_primitive())

    # Raise app error if property is an error tuple.
    if isinstance(property, tuple):
        raise AppError(context.errors.get(property[0]).format_message(property[1]))

    # Return response.
    return property