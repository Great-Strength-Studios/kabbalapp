from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Create new Domain Method Parameter instance from the input request data.
    domain_method_parameter = DomainMethodParameter.create(**context.data.to_primitive('domain_method_parameter.create'))

    # Get the app key from the headers.
    app_key = context.headers.get('app_key', None)

    # Load the Domain Repository from the service container.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Retrieve the Domain Model from the Domain Method parent id.
    domain_model = domain_repo.get_domain_model(context.data.parent_model_id)

    # Raise app error if the parent Domain Model does not exist.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(context.data.parent_model_id))
    
    # Retrieve the Domain Method from the parent Domain Model.
    domain_method = domain_model.get_method(context.data.method_name)

    # Raise app error if the Domain Method does not exist.
    if not domain_method:
        raise AppError(context.errors.DOMAIN_METHOD_NOT_FOUND.format_message(context.data.method_name, domain_model.id))
    
    # Check to see if the Domain Method already contains the Domain Method Parameter.
    exists = domain_method.has_parameter(domain_method_parameter)

    # Raise app error if the Domain Method contains the Domain Method Parameter to add.
    if exists:
        raise AppError(context.errors.DOMAIN_METHOD_PARAMETER_ALREADY_EXISTS.format_message(
            domain_method_parameter.name, 
            domain_method.name, 
            domain_model.id
        ))
    
    # Add the Domain Method Parameter to the Domain Method.
    domain_method.add_parameter(domain_method_parameter)

    # If the Domain Method Parameter is a model type, add a method parameter dependency to the Domain Model.
    if domain_method_parameter.type == MODEL_TYPE:
        inner_domain_model = domain_repo.get_domain_model(domain_method_parameter.inner_type)
        if not inner_domain_model:
            raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(domain_method_parameter.inner_type))
        domain_model.add_dependency(d.DomainModelDependency.create(
            model_id=inner_domain_model.id,
            class_name=inner_domain_model.class_name,
            dependency_type=METHOD_PARAMETER_DEPENDENCY
        ))

    # If the Domain Method Parameter is a list or dict type with a model inner type, add a method parameter dependency to the Domain Model.
    if domain_method_parameter.type in [LIST_TYPE, DICT_TYPE] and domain_method_parameter.inner_type_model_id is not None:
        inner_domain_model = domain_repo.get_domain_model(domain_method_parameter.inner_type_model_id)
        if not inner_domain_model:
            raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(domain_method_parameter.inner_type_model_id))
        domain_model.add_dependency(d.DomainModelDependency.create(
            model_id=inner_domain_model.id,
            class_name=inner_domain_model.class_name,
            dependency_type=METHOD_PARAMETER_DEPENDENCY
        ))
    
    # Save the parent Domain Model.
    domain_repo.save_domain_model(domain_model)

    # Return the added Domain Method Parameter.
    return domain_method_parameter