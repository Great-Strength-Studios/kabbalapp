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
    add_modules = {
        'modules/__init__.py': None,
        'repo/__init__.py': None,
        '__init__.py': """from .value_objects import *
            from .entities import *
            from .factory import *
            from .modules import *
            from .repo import *""",
        'entities.py': """from schematics import types as t, Model
            from schematics.transforms import whitelist, blacklist
            from schematics.types.serializable import serializable""",
        'factory.py': """from .entities import *
            from .modules import *""",
        'value_objects.py': """from schematics import types as t, Model
            from schematics.transforms import whitelist, blacklist
            from schematics.types.serializable import serializable""",
        'interfaces/__init__.py': """from .comands import *""",
        'interfaces/commands.py': """from schematics import types as t, Model
            from schematics.transforms import blacklist, whitelist""",
        'interfaces/services.py': None
    }

    # Load blocks.
    blocks = [app_printer.read_block(module, base_path='app') for module in core_modules]

    # Load blocks from add_modules.
    for module, content in add_modules.items():
        # Check if module exists.
        if target_app_printer.block_exists(module, base_path='app'):
            continue
        # Replace content with empty string if content is None.
        if content is None:
            content = ''
        blocks.append[target_app_printer.new_block('app', module, content)]

        # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)