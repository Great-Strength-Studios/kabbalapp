from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    ## Nothing to unpack right now.

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise app error if app key is null.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get app project manager.
    app_project_manager: p.AppProjectManager = context.services.app_project_manager()

    # Get app project.
    app_project = app_project_manager.load_project(app_key)

    # Get domain repository.
    domain_repo: DomainRepository = context.services.domain_repo(app_key)

    # Get all value objects.
    value_objects = domain_repo.get_value_objects()

    # Create new value object block instance.
    value_object_block = ValueObjectBlock.create(app_project.app_directory, value_objects)

    # Write value object block to file.
    with open(value_object_block.file_path, 'w') as f:
        f.write(value_object_block.print())