def default(request, app_context, **kwargs):
    # Get app key.
    app_key = request.get('app_key', None)
    
    # Return if app key is null.
    if not app_key:
        return

    # Get app project manager.
    from ...domains import p
    manager: p.AppProjectManager = app_context.container.app_project_manager()

    # Get app project.
    app_project = manager.load_project(app_key)

    # Return header data.
    return {
        'app_key': app_key,
        'app_directory': app_project.app_directory,
        'app_name': app_project.name,
        'app_version': app_project.version
    }

def app_project_headers(request, app_context, **kwargs):
    return {}