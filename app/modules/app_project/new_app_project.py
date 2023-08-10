from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Get new app project request.
    request: NewAppProject = context.data

    # Get app version from headers.
    version = context.headers.get('app_version', None)

    # Get app project manager.
    manager: p.AppProjectManager = context.services.app_project_manager()

    project = app_project.AppProject({
        'key': request.key,
        'app_directory': request.app_directory,
        'name': request.name,
        'version': version
    })

    # Save app project.
    manager.save_project(request.key, project)

    # Return app project.
    return project