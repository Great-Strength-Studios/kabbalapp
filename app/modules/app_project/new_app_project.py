from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Get new app project request.
    request: NewAppProject = context.data

    # Get app project manager.
    manager: AppProjectManager = context.services.app_project_manager()

    # Create app project.
    app_project = AppProject(request.to_primitive('app_project.map'))

    # Save app project.
    manager.save_project(request.app_key, app_project)

    # Return app project.
    return app_project