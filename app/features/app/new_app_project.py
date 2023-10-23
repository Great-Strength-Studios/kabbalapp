from ...core import *
from ...domain import *


REQUIREMENTS_CONTENT = """schematics>=2.1.1
pyyaml>=6.0.0
"""

# Add content to be written to the new modules.
CORE_ACTIVITY_CONTENT = """'''Activity Log Module'''
def handle(context):
    pass
"""

CORE_CONTAINERS_CONTENT = """from schematics import types as t, Model


# Container configuration
class ContainerConfiguration(Model):
    pass


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfiguration):
        # Default init
        self.config = config

        # Custom init below
        # ...
    

# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)
"""

DOMAIN_CONTENT = """from .models import *
from .factory import *
from .modules import *
from .repo import *
"""

DOMAIN_MODELS_CONTENT = """from ..core.domain import *
from .constants import *
"""

DOMAIN_FACTORY_CONTENT = """from .models import *
from .modules import *
"""

INTERFACES_CONTENT = """from .commands import *
"""

INTERFACES_COMMANDS_CONTENT = """from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist

from ..constants import *
"""

APP_CONSTANTS_CONTENT = """# Environment
APP_ENV = 'APP_ENV'
DEFAULT_APP_ENV = 'prod'

# Configuration file
APP_CONFIGURATION_FILE = '{}'

# Configuration
CONFIGS = 'configs' 
ENDPOINTS = 'endpoints'
ERRORS = 'errors'
"""

def handle(context: MessageContext):

    # Unpack data from request.
    name = context.data.name
    app_directory = context.data.app_directory
    tag = context.data.tag

    # Get app version from headers.
    version = context.headers.get('app_version', None)

    # Get app project manager.
    manager: app.AppProjectRepository = context.services.app_project_repo()

    project = app.AppProject.create(
        name=name,
        app_directory=app_directory,
        version=version,
        tag=tag
    )

    # Save app project.
    manager.save_project(project)

    # Load local app printer.
    app_printer: AppPrinter = context.services.app_printer()

    # Load target app printer.
    target_app_printer: AppPrinter = context.services.app_printer(tag)

    # Arrange packages/modules to be read.
    core_modules = [
        'core/config/__init__.py',
        'core/config/json.py',
        'core/config/yaml.py',
        'core/error.py',
        'core/routing.py',
        'core/domain.py',
        'core/__init__.py',
        '__init__.py'
    ]

    # Arrange packages/modules to be written to the domain package if they do not already exist.
    add_modules = {
        'core/activity.py': CORE_ACTIVITY_CONTENT,
        'core/containers.py': CORE_CONTAINERS_CONTENT,
        'domain/modules/__init__.py': '',
        'domain/repo/__init__.py': '',
        'domain/__init__.py': DOMAIN_CONTENT,
        'domain/factory.py': DOMAIN_FACTORY_CONTENT,
        'domain/models.py': DOMAIN_MODELS_CONTENT,
        'features/__init__.py': '',
        'interfaces/__init__.py': INTERFACES_CONTENT,
        'interfaces/commands.py': INTERFACES_COMMANDS_CONTENT,
        'interfaces/services.py': '',
        'constants.py': APP_CONSTANTS_CONTENT.format(project.schema_location),
    }

    # Load blocks.
    blocks = [app_printer.read_block(module, base_path='app') for module in core_modules]

    # Load blocks from add_modules.
    for module, content in add_modules.items():
        # Check if module exists.
        if target_app_printer.block_exists(module, base_path='app'):
            continue
        blocks.append(target_app_printer.new_block('app', module, content))

    # Add requirements.txt block.
    blocks.append(target_app_printer.new_block('', 'requirements.txt', REQUIREMENTS_CONTENT))

    # Add special block for app.yml.
    app_yml_block = target_app_printer.new_block('app', 'app.yml', '')
    app_yml_block.code_block = {
        'commands': {},
        'interfaces': {
            'types': {}
        },
        'errors': {},
        'features': {
            'groups': {},
        },
        'domain': {
            'modules': {},
            'repos': {},
            'models': {},
            'factories': {},
        },
    }
    blocks.append(app_yml_block)

    # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)

    # Return app project.
    return project