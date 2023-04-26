from ...core import *
from ...domains import *

def handle(context: MessageContext):
    # Get request event.
    request: AddDomain = context.data

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain service.
    service: d.AppDomainService = context.services.domain_service(app_key)

    # Create domain key if none exists.
    if not request.key:
        request.key = request.name.lower().replace(' ', '_')
    
    # Add domain.
    domain = service.add_domain(**request.to_primitive())

    # Raise app error if domain already exists.
    ## TODO - This should be a domain error.
    if isinstance(domain, tuple):
        raise AppError(context.errors.get(domain[0]).format_message(*domain[1:]))

    # Return domain.
    return domain