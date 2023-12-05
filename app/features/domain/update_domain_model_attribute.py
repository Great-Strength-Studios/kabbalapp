from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    model_id = context.data.model_id
    attribute_name = context.data.attribute_name
    attribute_setting = context.data.attribute_setting
    value = context.data.value

    # Get app project key.
    app_key = context.headers.get('app_key', None)
    
    # Get domain repository.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Get domain model.
    domain_model = domain_repo.get_domain_model(model_id)

    # Raise app error if domain model is not found.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(model_id))
    
    # Get domain model attribute.
    attribute = domain_model.get_attribute(attribute_name)

    # Raise app error if domain model attribute is not found.
    if not attribute:
        raise AppError(context.errors.DOMAIN_MODEL_ATTRIBUTE_NOT_FOUND.format_message(attribute_name, model_id))
    
    # Update attribute setting.
    attribute.update(attribute_setting, value)

    # Save domain model.
    domain_repo.save_domain_model(domain_model)

    # Return updated attribute.
    return attribute