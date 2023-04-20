from ...core import *

def handle(context: MessageContext):
    from ...domains import AppProjectManager, AppPrinter
    
    # Load request.
    request: SyncAppProject = context.data

    # Load local app printer.
    app_printer: AppPrinter = context.services.app_printer()

    # Load target app printer.
    target_app_printer: AppPrinter = context.services.app_printer(request.app_key)

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

    # Load blocks.
    blocks = [app_printer.read_block(module) for module in modules]

    # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)