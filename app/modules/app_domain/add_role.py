from ...core import *

def handle(context: MessageContext):

    # Unpack request.
    request: AddDomainRole = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Import domain.
    from ...domains import app_domain as dom

    # Get domain service.
    domain_service: dom.DomainService = context.services.domain_service(app_key)

    # Get domain.
    domain: dom.DomainEntity = dom.get_domain(domain_service, request.domain_key)

    # Add role.
    role = domain.add_role(request.key, request.type, request.fields)

    # Return response.
    return role