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
    modules = [
        'app/core/config/__init__.py',
        'app/core/config/json.py',
        'app/core/config/yaml.py',
        'app/core/error.py',
        'app/core/routing.py',
        'app/core/__init__.py',
        'app/__init__.py'
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
    blocks = [app_printer.read_block(module) for module in modules]

    # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)