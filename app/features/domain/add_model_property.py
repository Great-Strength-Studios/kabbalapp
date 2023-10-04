from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    model_id = context.data.model_id
    name = context.data.name
    type = context.data.type
    inner_type = context.data.inner_type
    required = context.data.required
    default = context.data.default
    choices = context.data.choices
    description = context.data.description
    type_properties = context.data.type_properties

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get domain repository.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # First check to see if the domain model exists.
    domain_model = domain_repo.get_domain_model(model_id)

    # Raise app error if domain model does not exist.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(model_id))

    # Create type properties
    try:
        type_properties = create_type_properties(type, **type_properties)
    # Raise a invalid type property error if the type property is invalid.
    except TypeError as e:
        import re
        invalid_arg = re.search(r"unexpected keyword argument '(.*)'", str(e)).group(1)
        raise AppError(context.errors.INVALID_TYPE_PROPERTY.format_message(type, invalid_arg))


    # Create a new model property
    property = d.DomainModelProperty.create(
        name=name,
        type=type,
        inner_type=inner_type,
        required=required,
        default=default,
        choices=choices,
        description=description,
        type_properties=type_properties
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