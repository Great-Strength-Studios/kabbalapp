from ...core import *
from ...domains import *

def handle(context: MessageContext):
    import os

    # Get request event.
    request: AddDomain = context.data

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain service.
    service: DomainService = context.services.domain_service(app_key)

    # Create domain key if none exists.
    if not request.key:
        request.key = request.name.to_lower().replace(' ', '-')
    
    # Add domain.
    domain = service.add_domain(request.name, request.key)

    # Return domain.
    return domain