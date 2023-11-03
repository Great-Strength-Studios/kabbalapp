from ...core import *
from ...domain import *

def handle(context: MessageContext):
    
    # Get app project manager.
    app_project_repo: app.AppProjectRepository = context.services.app_project_repo()

    # Verify that the app project exists.
    if not app_project_repo.project_exists(context.data.id):
        raise AppError(context.errors.APP_PROJECT_NOT_FOUND.format_message(context.data.id))

    # Set default project.
    app_project_repo.set_default_app_project(context.data.id)

    # Return response.
    return context.data.id