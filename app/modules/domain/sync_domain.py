from ...core import *
from ...domain import *

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

    # Format domain package directory.
    domain_package_dir = os.path.join(app_directory, 'app', 'domains')

    # Format domain directory.
    domain_dir = os.path.join(domain_package_dir, domain.key)

    # Make directories even if they exist.
    os.makedirs(domain_dir, exist_ok=True)

    # Write files.
    for file_name, file_lines in files.items():
        file_path = os.path.join(domain_dir, file_name)
        if not os.path.exists(file_path) or request.force:
            with open(file_path, 'w') as f:
                f.write('\n'.join(file_lines))

    # Add domain import to app domains __init__.py file.
    app_domains_init_file_path = os.path.join(domain_package_dir, '__init__.py')
    with open(app_domains_init_file_path, 'r') as f:
        data = f.readlines()
    import_format = 'from . import {}'.format(domain.key)
    if domain.aliases:
        import_format += ', ' + ', '.join(['{} as {}'.format(domain.key, alias) for alias in domain.aliases])
    domain_import_found = False
    for i in range(len(data)):
        line = data[i]
        if domain.key in line:
            data[i] = import_format
            domain_import_found = True
            break
    if not domain_import_found:
        data.append(import_format)
    with open(app_domains_init_file_path, 'w') as f:
        data = '\n'.join(data)
        f.writelines(data)