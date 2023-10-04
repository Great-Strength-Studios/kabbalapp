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
    domain_models = domain_repo.get_domain_models()

    # Create new value object block instance.
    model_block = block.AppDomainModelBlock.create(app_project.app_directory, domain_models)

    # Write block to file.
    with open(model_block.file_path, 'w') as f:
        f.write(model_block.print())