def default(request, app_context, **kwargs):

    # Get app project manager.
    from ....domain import p
    manager: p.AppProjectManager = app_context.container.app_project_manager()

    # Get app key.
    app_key = request.get('app_key', None)

    # Get app project.
    app_project = manager.load_project(app_key)

    # Get version from kwargs.
    version = kwargs.get('version', None)

    # Return header data.
    return {
        'app_key':  app_key if app_key else app_project.key,
        'app_directory': app_project.app_directory,
        'app_name': app_project.name,
        'app_version': app_project.version if app_project.version else version
    }

def app_project_headers(request, app_context, **kwargs):
    return {
        'app_version': kwargs.get('version', None)
    }