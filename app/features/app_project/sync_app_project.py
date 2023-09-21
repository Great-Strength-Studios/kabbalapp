from ...core import *
from ...domain import *

def handle(context: MessageContext):    
    # Load request.
    request = context.data

    # Load local app printer.
    app_printer: AppPrinter = context.services.app_printer()

    # Load target app printer.
    target_app_printer: AppPrinter = context.services.app_printer(request.key)

    # Arrange packages/modules to be read.
    core_modules = [
        'core/config/__init__.py',
        'core/config/json.py',
        'core/config/yaml.py',
        'core/error.py',
        'core/routing.py',
        'core/__init__.py',
        '__init__.py'
    ]

    # Arrange packages/modules to be written to the domain package if they do not already exist.
    add_domain_modules = [
        'modules/__init__.py',
        'repo/__init__.py',
        '__init__.py',
        'entities.py',
        'factory.py',
        'value_objects.py',
    ]

    # Arrange packages/modules to be written to the interfaces package if they do not already exist.
    add_interface_modules = [
        '__init__.py',
        'commands.py',
        'services.py',
    ]

    # Load blocks.
    blocks = [app_printer.read_block(module, base_path='app') for module in core_modules]

    # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)