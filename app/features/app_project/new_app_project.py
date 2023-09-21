from ...core import *
from ...domain import *
from ...interfaces import *

def handle(context: MessageContext):

    # Get new app project request.
    request: NewAppProject = context.data

    # Get app version from headers.
    version = context.headers.get('app_version', None)

    # Get app project manager.
    manager: p.AppProjectManager = context.services.app_project_manager()

    

    project = app_project.AppProject({
        'key': request.key,
        'app_directory': request.app_directory,
        'name': request.name,
        'version': version
    })

    # Save app project.
    manager.save_project(request.key, project)

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

    # Add content to be written to the new modules.
    CORE_ACTIVITY_CONTENT = """
    '''Activity Log Module'''
    def handle(context):
        pass
    """

    CORE_CONTAINERS_CONTENT = """
    from schematics import types as t, Model

    from ..services import SkyWellness, ConfigurationService

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

    

    DOMAIN_CONTENT = """
    from .value_objects import *
    from .entities import *
    from .factory import *
    from .modules import *
    from .repo import *
    """

    DOMAIN_ENTITIES_CONTENT = """
    from schematics import types as t, Model
    from schematics.transforms import whitelist, blacklist
    from schematics.types.serializable import serializable
    """

    DOMAIN_VALUE_OBJECTS_CONTENT = """
    from schematics import types as t, Model
    from schematics.transforms import whitelist, blacklist
    from schematics.types.serializable import serializable
    """

    DOMAIN_FACTORY_CONTENT = """
    from .value_objects import *
    from .entities import *
    from .modules import *
    """

    INTERFACES_CONTENT = """
    from .commands import *
    """

    INTERFACES_COMMANDS_CONTENT = """
    from schematics import types as t, Model
    from schematics.transforms import blacklist, whitelist
    """

    APP_CONSTANTS_CONTENT = """
    # Environment
    APP_ENV = 'APP_ENV'
    DEFAULT_APP_ENV = 'prod'

    # Configuration file
    CONFIG_FILE_DIRECTORY = 'app/{}'
    APP_SCHEMA_FILE = 'app.yml'

    # Configuration
    CONFIGS = 'configs' 
    ENDPOINTS = 'endpoints'
    ERRORS = 'errors'
    """

    # Arrange packages/modules to be written to the domain package if they do not already exist.
    add_modules = {
        'core/activity.py': CORE_ACTIVITY_CONTENT,
        'domain/modules/__init__.py': None,
        'domain/repo/__init__.py': None,
        'domain/__init__.py': DOMAIN_CONTENT,
        'domain/entities.py': DOMAIN_ENTITIES_CONTENT,
        'domain/factory.py': DOMAIN_FACTORY_CONTENT,
        'domain/value_objects.py': DOMAIN_VALUE_OBJECTS_CONTENT,
        'features/__init__.py': None,
        'interfaces/__init__.py': INTERFACES_CONTENT,
        'interfaces/commands.py': INTERFACES_COMMANDS_CONTENT,
        'interfaces/services.py': None,
        'constants.py': APP_CONSTANTS_CONTENT,
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
        blocks.append(target_app_printer.new_block('app', module, content))

    # Add requirements.txt block.
    REQUIREMENTS_CONTENT = """
    schematics>=2.1.1
    pyyaml>= 6.0
    """
    blocks.append(target_app_printer.new_block('', 'requirements.txt', REQUIREMENTS_CONTENT))

    # Add special block for app.yml.
    app_yml_block = target_app_printer.new_block('app', 'app.yml', '')
    app_yml_block.code_block = {
        'commands': {},
        'interfaces': {},
        'errors': {},
        'features': {
            'groups': {},
        },
        'domain': {
            'modules': {},
            'repos': {},
            'entities': {},
            'value_objects': {},
            'factories': {},
        },
    }
    blocks.append(app_yml_block)

    # Write blocks.
    for block in blocks:
        target_app_printer.print_block(block)

    # Return app project.
    return project