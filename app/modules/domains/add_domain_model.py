from ...core import *

def handle(context: MessageContext):

    # Get request.
    request = context.data

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain service with app key input.
    from ...domains import domain as dom
    service: dom.DomainService = context.services.domain_service(app_key)

    # Create domain model key if none exists.
    if not request.key:
        request.key = request.name.lower().replace(' ', '_')
    
    # Get requested domain.
    domain: dom.DomainEntity = dom.get_domain(service, request.domain_key)

    # Add domain model to domain.
    model = domain.add_model(request.key, request.name)

    # Return domain model.
    return model