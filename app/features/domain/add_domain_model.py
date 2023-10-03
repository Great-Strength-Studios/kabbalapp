from ...core import *
from ...domain import *

def handle(context: MessageContext):
    
    # Unpack request.
    name = context.data.name
    class_name = context.data.class_name
    type = context.data.type

    # Get app project key.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)

    # Get domain repository.
    domain_repo: DomainRepository = context.services.domain_repo(app_key)

    # Create new value object instance.
    domain_model = AppDomainModel.create(name=name, type=type, class_name=class_name)

    # Check to see if existing domain model exists.
    existing_model = domain_repo.get_domain_model(domain_model.id)

    # Raise Value Object already exists error if value object already exists.
    if existing_model:
        raise AppError(context.errors.DOMAIN_MODEL_ALREADY_EXISTS.format_message(domain_model.type, domain_model.class_name))

    # Add value object to domain and to value objects list.
    domain_repo.save_domain_model(domain_model)

    # Return added value object.
    return domain_model