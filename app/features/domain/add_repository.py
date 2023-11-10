from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Create new App Repository instance from the input request data.
    app_repo = AppRepository.create(**context.data.to_primitive())

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Load the Domain Repository from the service container.
    domain_repo: d.DomainRepository = context.services.domain_repo(app_key)

    # Check to see if the Domain Repository already contains the App Repository.
    existing_repo = domain_repo.get_repository(app_repo.id)

    # Raise app error if the Domain Repository contains the App Repository to add.
    if existing_repo:
        raise AppError(context.errors.REPOSITORY_ALREADY_EXISTS.format_message(app_repo.id))
    
    # Save the App Repository to the Domain Repository.
    domain_repo.save_repository(app_repo)

    # Return the added App Repository.
    return app_repo