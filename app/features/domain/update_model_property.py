from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    model_id = context.data.model_id
    property_name = context.data.property_name
    property_setting = context.data.property_setting
    value = context.data.value

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get domain repository.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Get domain model.
    domain_model = domain_repo.get_domain_model(model_id)

    # Raise app error if domain model is not found.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(model_id))
    
    # Get domain model property.
    property = domain_model.get_property(property_name)

    # Raise app error if domain model property is not found.
    if not property:
        raise AppError(context.errors.DOMAIN_MODEL_PROPERTY_NOT_FOUND.format_message(property_name, model_id))
    
    # Update property setting.
    property.update(property_setting, value)

    # Save domain model.
    domain_repo.save_domain_model(domain_model)

    # Return updated property.
    return property