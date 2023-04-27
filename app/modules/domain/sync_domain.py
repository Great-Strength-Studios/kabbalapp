from ...core import *
from ...domains import *

def handle(context: MessageContext):
    import os

    # Unpack request.
    request: SyncDomain = context.data

    # Retreive app key from headers.
    app_key = context.headers.get('app_key', None)

    # Raise error if app key is not provided.
    if app_key is None:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get domain service.
    domain_service: d.AppDomainService = context.services.domain_service(app_key)

    # Get domain.
    domain = domain_service.get_domain(request.domain_key)
    if isinstance(domain, tuple):
        raise context.errors.get(domain[0]).format_message(domain[1])

    # File lines
    init_file = [
        'from .services import *',
    ]
    services_file = [
        'from .models import *',
    ]
    models_file = [
        'from typing import List',
        'from schematics import types as t, Model',
        'from schematics.transforms import whitelist, blacklist',
        'from schematics.types.serializable import serializable',
    ]
    files = {
        '__init__.py': init_file,
        'services.py': services_file,
        'models.py': models_file
    }

    # Get app directory from headers.
    app_directory = context.headers.get('app_directory')

    # Format domain directory.
    domain_directory = os.path.join(app_directory, 'app', 'domains', domain.key)

    # Make directories even if they exist.
    os.makedirs(domain_directory, exist_ok=True)

    # Write files.
    for file_name, file_lines in files.items():
        file_path = os.path.join(domain_directory, file_name)
        if not os.path.exists(file_path) or request.force:
            with open(file_path, 'w') as f:
                f.write('\n'.join(file_lines))