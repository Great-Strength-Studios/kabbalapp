from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    tag = context.data.tag
    
    # Get app project manager.
    app_project_repo: app.AppProjectRepository = context.services.app_project_repo()

    # Verify that the app project exists.
    if not app_project_repo.project_exists(tag):
        raise AppError(context.errors.APP_PROJECT_NOT_FOUND.format_message(tag))

    # Set default project.
    app_project_repo.set_default_app_project(tag)

    # Return response.
    return tag