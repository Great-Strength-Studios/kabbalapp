from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Create new Domain Method instance from the input request data.
    domain_method = d.DomainMethod.create(**context.data.to_primitive('domain_method.create'))

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Load the Domain Repository from the service container.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Retrieve the Domain Model from the Domain Method parent id.
    domain_model = domain_repo.get_domain_model(context.data.parent_id)

    # Raise app error if the parent Domain Model does not exist.
    if not domain_model:
        raise AppError(context.errors.DOMAIN_MODEL_NOT_FOUND.format_message(context.data.parent_id))
    
    # Check to see if the Domain Model already contains the Domain Method.
    exists = domain_model.has_method(domain_method)

    # Raise app error if the parent Domain model contains the Domain method to add.
    if exists:
        raise AppError(context.errors.DOMAIN_METHOD_ALREADY_EXISTS.format_message(domain_method.name, domain_model.id))
    
    # If the domain method return type or inner return type is a model, then we need to set the model id.
    if domain_method.return_type == MODEL_TYPE or domain_method.inner_return_type == MODEL_TYPE:
        return_type_model = domain_repo.get_domain_model(domain_method.return_type_model_id)
        # Raise app error if the return type model does not exist.
        if not return_type_model:
            raise AppError(context.errors.DOMAIN_MODEL_RETURN_TYPE_NOT_FOUND.format_message(domain_method.method_name, domain_method.return_type_model_id))
        # Create a new method-type domain model dependency and add it to the domain model.
        dependency = d.DomainModelDependency.create(
            model_id=return_type_model.id,
            class_name=return_type_model.class_name,
            dependency_type=METHOD_DEPENDENCY
        )
        domain_model.add_dependency(dependency)

    # Add the Domain Method to the parent Domain Model.
    domain_model.add_method(domain_method)

    # Save the parent Domain Model.
    domain_repo.save_domain_model(domain_model)

    # Return the added Domain Method.
    return domain_method