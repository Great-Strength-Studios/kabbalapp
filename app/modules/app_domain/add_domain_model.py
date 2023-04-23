from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Get request.
    request: AddDomainModel = context.data

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain service with app key input.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Create domain model key if none exists.
    if not request.key:
        request.key = request.name.lower().replace(' ', '_')

    # Add app domain model.
    model = domain_service.add_model(**request.to_primitive()) 

    # Return domain model.
    return model