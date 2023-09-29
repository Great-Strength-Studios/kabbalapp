from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    model_id = context.data.model_id
    name = context.data.name
    type = context.data.type
    required = context.data.required
    default = context.data.default
    choices = context.data.choices
    description = context.data.description

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get domain repository.
    domain_repo: DomainRepository = context.services.domain_repo(app_key)

    # First check to see if the domain model exists.
    domain_model = domain_repo.get_domain_model(model_id)

    # Raise app error if domain model does not exist.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(model_id))

    # Create a new model property
    property = DomainModelProperty.create(
        name=name,
        type=type,
        required=required,
        default=default,
        choices=choices,
        description=description
    )

    # Check to see if property already exists on the model.
    exists = domain_model.has_property(property)

    # Raise app error if property already exists.
    if exists:
        raise AppError(context.errors.DOMAIN_MODEL_PROPERTY_ALREADY_EXISTS.format_message(property.name))

    # Add property to model.
    domain_model.add_property(property)

    # Save domain model.
    # TODO: Change this once things are in proper order
    domain_repo.save_value_object(domain_model)

    # Return response.
    return property