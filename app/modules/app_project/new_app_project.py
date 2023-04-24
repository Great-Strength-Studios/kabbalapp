from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Get new app project request.
    request: NewAppProject = context.data

    # Get app project manager.
    manager: p.AppProjectManager = context.services.app_project_manager()

    # Save app project.
    manager.save_project(request.app_key, **request.to_primitive('app_project.map'))

    # Return app project.
    return app_project