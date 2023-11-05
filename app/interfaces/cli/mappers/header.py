def default(request, app_context, **kwargs):

    # Load app module from domain.
    from ....domain import app

    # Load app error from core.
    from ....core import AppError

    # Load app project repo.
    app_project_repo: app.AppProjectRepository = app_context.container.app_project_repo()

    # Get app key from the incoming request.
    app_key = request.get('app_key', None)

    # Raise the app key required error if the app key is null and the default app project is not configured.
    if not app_key and not app_project_repo.default_app_project_configured():
        raise AppError(app_context.errors.APP_KEY_REQUIRED)

    # Get app project.
    app_project = app_project_repo.load_project(app_key)

    # Raise app project not found error if no app project is returned.
    if not app_project:
        raise AppError(app_context.errors.APP_PROJECT_NOT_FOUND.format_message(app_key))

    # Get version from kwargs.
    version = kwargs.get('version', None)

    # Return header data.
    return {
        'app_key':  app_key if app_key else app_project.id,
        'app_directory': app_project.app_directory,
        'app_name': app_project.name,
        'app_version': app_project.version if app_project.version else version
    }

def app_project_headers(request, app_context, **kwargs):
    return {
        'app_version': kwargs.get('version', None)
    }