from ...core import *
from ...domains import *

def handle(context: MessageContext):

    # Unpack request.
    request: SetDefaultAppProject = context.data
    
    # Get app project manager.
    proj_manager: p.AppProjectManager = context.services.app_project_manager()

    # Set default project.
    property = proj_manager.set_default_app_project(request.app_key)

    # Raise app error if property is an error tuple.
    if isinstance(property, tuple):
        raise AppError(context.errors.get(property[0]).format_message(property[1]))

    # Return response.
    return request.app_key