from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    parent_model_id = context.data.parent_model_id
    name = context.data.name
    type = context.data.type
    inner_type = context.data.inner_type
    inner_type_model_id = context.data.inner_type_model_id
    poly_type_model_ids = context.data.poly_type_model_ids
    required = context.data.required
    default = context.data.default
    choices = context.data.choices
    description = context.data.description
    type_properties = context.data.type_properties

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)
    
    # Get domain repository.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # First check to see if the domain model exists.
    domain_model = domain_repo.get_domain_model(parent_model_id)

    # Raise app error if domain model does not exist.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(parent_model_id))

    # Create type properties
    try:
        type_properties = create_type_properties(type, **type_properties)
    # Raise a invalid type attribute error if the type attribute is invalid.
    except TypeError as e:
        import re
        invalid_arg = re.search(r"unexpected keyword argument '(.*)'", str(e)).group(1)
        raise AppError(context.errors.INVALID_TYPE_PROPERTY.format_message(type, invalid_arg))

    # If the type is a value_object, verify that the value object exists.
    if type == MODEL_TYPE:
        value_object = domain_repo.get_domain_model(inner_type)
        if not value_object:
            raise AppError(context.errors.DOMAIN_MODEL_ATTRIBUTE_INNER_TYPE_NOT_FOUND.format_message(inner_type))
        # Add value object as dependency
        dependency = d.DomainModelDependency.create(
            model_id=inner_type,
            class_name=value_object.class_name,
            module=None
        )
        domain_model.add_dependency(dependency)

    # If the inner type is a value object, verify that the inner type exists.
    elif inner_type == MODEL_TYPE:
        value_object = domain_repo.get_domain_model(inner_type_model_id)
        if not value_object:
            raise AppError(context.errors.DOMAIN_MODEL_ATTRIBUTE_INNER_TYPE_NOT_FOUND.format_message(inner_type_model_id))
        # Add value object as dependency
        dependency = d.DomainModelDependency.create(
            model_id=inner_type_model_id,
            class_name=value_object.class_name,
            dependency_type='attribute'
        )
        domain_model.add_dependency(dependency)
    
    # If the type is a poly, verify that the poly types exist.
    elif type == POLY_TYPE:
        for poly_type_model_id in poly_type_model_ids:
            poly_type = domain_repo.get_domain_model(poly_type_model_id)
            if not poly_type:
                raise AppError(context.errors.DOMAIN_MODEL_ATTRIBUTE_INNER_TYPE_NOT_FOUND.format_message(poly_type_model_id))
            # Add poly type as dependency
            dependency = d.DomainModelDependency.create(
                model_id=poly_type_model_id,
                class_name=poly_type.class_name,
                dependency_type='attribute'
            )
            domain_model.add_dependency(dependency)

    # Create a new model attribute
    attribute = d.DomainModelAttribute.create(
        name=name,
        type=type,
        inner_type=inner_type,
        inner_type_model_id=inner_type_model_id,
        poly_type_model_ids=poly_type_model_ids,
        required=required,
        default=default,
        choices=choices,
        description=description,
        type_properties=type_properties
    )

    # Check to see if attribute already exists on the model.
    exists = domain_model.has_attribute(attribute.name)

    # Raise app error if attribute already exists.
    if exists:
        raise AppError(context.errors.DOMAIN_MODEL_ATTRIBUTE_ALREADY_EXISTS.format_message(attribute.name))

    # Add attribute to model.
    domain_model.add_attribute(attribute)

    # Save domain model.
    domain_repo.save_domain_model(domain_model)

    # Return response.
    return attribute