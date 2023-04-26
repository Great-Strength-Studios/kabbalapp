from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Unpack request.
    request: UpdateDomain = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get app domain service.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Update domain.
    domain = domain_service.update_domain(**request.to_primitive())

    # Raise app error if domain is an error tuple.
    if isinstance(domain, tuple):
        raise AppError(context.errors.get(domain[0]).format_message(domain[1]))
    
    # Return response.
    return domain