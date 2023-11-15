from ...core import *
from ...domain import *

def handle(context: MessageContext):
    
    # Create new repository implementation instance.
    repo_impl = AppRepositoryImplementation.create(**context.data.to_primitive('app_repository_implementation.create'))

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Get domain repository.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Retrieve the domain repository instance from the domain repository.
    domain_repo_instance = domain_repo.get_repository(context.data.repository_id)

    # Raise app error if domain repository does not exist.
    if not domain_repo_instance:
        raise AppError(context.errors.REPOSITORY_NOT_FOUND.format_message(context.data.repository_id))
    
    # Add the repository implementation to the domain repository.
    domain_repo_instance.add_implementation(repo_impl)

    # Save the domain repository.
    domain_repo.save_repository(domain_repo_instance)

    # Return the repository implementation.
    return repo_impl