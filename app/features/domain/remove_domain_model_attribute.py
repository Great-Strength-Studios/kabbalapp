from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack the context request data.
    parent_model_id = context.data.parent_model_id
    attribute_name = context.data.attribute_name

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Get domain repository.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Get domain model.
    domain_model = domain_repo.get_domain_model(parent_model_id)

    # Raise app error if domain model is not found.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(parent_model_id))
    
    # Get model attribute.
    attribute = domain_model.get_attribute(attribute_name)
    
    # Raise app error if domain model attribute is not found.
    if not attribute:
        raise AppError(context.errors.DOMAIN_MODEL_ATTRIBUTE_NOT_FOUND.format_message(attribute_name, parent_model_id))
    
    # Remove model attribute.
    domain_model.remove_attribute(attribute)

    # Save domain model.
    domain_repo.save_domain_model(domain_model)
    
    # Return the response.
    return attribute