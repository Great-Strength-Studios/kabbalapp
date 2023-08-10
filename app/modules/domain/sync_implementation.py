from ...core import *
from ...domain import *

def handle(context: MessageContext):

    # Unpack request.
    request: SyncDomainImplementation = context.data\
    
    # Get app key from headers.
    app_key = context.headers.get('app_key', None)

    # If app key is not provided, raise exception.
    if not app_key:
        raise AppError(context.errors.APP_KEY_REQUIRED)
    
    # Get domain service.
    service: d.AppDomainService = context.services.domain_service(app_key)

    # Get domain implementation.
    implementation = service.get_implementation(request.domain_key, request.implementation_key)

    # If domain implementation does not exist, raise exception.
    if isinstance(implementation, tuple):
        raise AppError(context.errors.get(implementation[0]).format_message(*implementation[1:]))
    
    # Get domain implementation directory.
    import os
    implementation_root_dir = os.path.join(
        context.headers.get('app_directory'),
        'app',
        'domains',
        request.domain_key,
        'impl')
    
    implementation_dir = os.path.join(
        implementation_root_dir,
        implementation.key)
    
    # Make directories even if they exist.
    os.makedirs(implementation_dir, exist_ok=True)

    # Format data for implementation files.
    impl_file_data = {
        '__init__.py': [
            'from .services import *',
        ],
        'services.py': [
            'from .models import *',
            'from ...services import *',
        ],
        'models.py': [
            'from ...models import *',
        ]
    }

    # Write files.
    for file_name, file_lines in impl_file_data.items():
        file_path = os.path.join(implementation_dir, file_name)
        if not os.path.exists(file_path) or request.force:
            with open(file_path, 'w') as f:
                f.write('\n'.join(file_lines))

    # Add implementation import to domain implementation __init__.py file.
    init_file_path = os.path.join(implementation_root_dir, '__init__.py')
    with open(init_file_path, 'r') as f:
        data = f.read()
    if 'from .{} import *'.format(implementation.key) in data:
        return
    with open(init_file_path, '+a') as f:
        f.write('\nfrom .{} import *'.format(implementation.key))