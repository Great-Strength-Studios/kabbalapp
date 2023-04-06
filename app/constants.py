
# Environment
APP_ENV = 'APP_ENV'
DEFAULT_APP_ENV = 'prod'
PROJECTS_FILE_PATH = 'PROJECTS_FILE_PATH'
DEBUG = 'DEBUG'

# Configuration file
APP_CONFIGURATION_FILE = 'app/app.yml'

# Configuration
CONFIGS = 'configs' 
ENDPOINTS = 'endpoints'
ERRORS = 'errors'

# Printing direcories
APP_DIR_NAME = 'app'
CORE_DIR_NAME = 'core'
CORE_MAPPINGS_DIR_NAME = 'mappings'
ENDPOINTS_DIR_NAME = 'endpoints'
MODULES_DIR_NAME = 'modules'
SERVICES_DIR_NAME = 'services'

# Printing files
INIT_FILE = '__init__.py'
REQUIREMENTS_FILE = 'requirements.txt'
APP_CONFIG_FILE = 'app.yml'
APP_CONSTANTS_FILE = 'constants.py'
CORE_MAPPINGS_DATA_FILE = 'data.py'
CORE_MAPPINGS_HEADERS_FILE = 'headers.py'
CORE_MAPPINGS_SERVICES_FILE = 'services.py'
CORE_ACTIVITY_FILE = 'activity.py'
CORE_CONTAINERS_FILE = 'containers.py'
CORE_ERROR_FILE = 'error.py'
CORE_EVENTS_FILE = 'events.py'
CORE_ROUTING_FILE = 'routing.py'

# Printing file content
REQUIREMENTS_CONTENT = """
schematics>=2.1.1
pyyaml>= 6.0
"""

APP_INIT_CONTENT = """
import os, yaml

from .constants import *
from .core import AppBuilder


def load_app_config(builder: AppBuilder):
    from .core import AppConfig, EndpointConfig, Error

    lang = os.getenv('LANG', 'en_US')
    lang = lang.split('.')[0]

    with open(CONFIG_FILE_DIRECTORY.format(APP_SCHEMA_FILE)) as stream:
        app_components = yaml.safe_load(stream)

    endpoints = {}
    try:
        for k, v in app_components[ENDPOINTS].items():
            endpoints[k] = EndpointConfig(v)
    # Throw exception if no endpoints configured
    except AttributeError:
        pass
    errors = {}
    try:
        for k, v in app_components[ERRORS].items():
            v['error_name'] = k
            errors[k] = Error(v)
    except TypeError:
        pass
        
    app_config = AppConfig(endpoints, errors)
    builder.set_app_config(app_config)

def load_container_config(builder: AppBuilder):
    from .core import ContainerConfiguration

    container_config = ContainerConfiguration()
    container_config.validate()
"""

APP_CONFIG_CONTENT = {
    'endpoints': {},
    'errors': {},
    'events': {},
    'mappings': {
        'data': {},
        'header': {},
        'service': {}
    },
    'modules': {},
    'services': {},
}

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

CORE_MAPPINGS_DATA_CONTENT = """
from ..events import *
"""

CORE_MAPPINGS_HEADERS_CONTENT = """
def default(request, app_context, **kwargs):
    pass
"""

CORE_INIT_CONTENT = """
from typing import Dict

from .error import *
from .containers import *
from .routing import *
from .events import *

class AppConfig():

    endpoints: Dict[str, EndpointConfig] = {}
    errors: Dict[str, Error] = {}

    def __init__(self, 
        endpoints: Dict[str, EndpointConfig] = {}, 
        errors: Dict[str, Error] = {}): 

        self.endpoints = endpoints
        self.errors = errors


class AppContext():

    name: str = None
    container_config: ContainerConfiguration = None
    container: Container = None
    errors: ErrorManager = ErrorManager()
    endpoints: dict = None
    
    def __init__(self, name: str, app_config: AppConfig, container_config: ContainerConfiguration):
        self.name = name
        self._load_errors(app_config)
        self._load_endpoints(app_config)
        self._load_container(container_config)

    def _load_errors(self, app_config: AppConfig) -> None:
        for error in app_config.errors.values():
            self.errors.add(error)

    def _load_endpoints(self, app_config: AppConfig) -> None:
        self.endpoints = app_config.endpoints

    def _load_container(self, container_config: ContainerConfiguration) -> None:
        self.container_config = container_config
        self.container = Container(container_config)

    def run(self, **kwargs):
        pass


class AppBuilder():

    class Session():
        name: str = None
        app_config: AppConfig = None
        container_config: ContainerConfiguration = None

    _current_session = None

    @property
    def app_config(self) -> AppConfig:
        return self._current_session.app_config

    def create_new_app(self, name: str, **kwargs):
        kwargs
        if self._current_session:
            self._current_session = None
        self._current_session = self.Session()
        self._current_session.name = name
        return self

    def set_app_config(self, app_config: AppConfig):
        self._current_session.app_config = app_config
        return self

    def set_container_config(self, container_config: ContainerConfiguration):
        self._current_session.container_config = container_config
        return self

    def build(self):
        pass
"""

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

CORE_ERROR_CONTENT = """
from schematics import types as t, Model
from schematics.transforms import whitelist

class Error(Model):

    error_code = t.StringType(required=True)
    error_name = t.StringType(required=True)
    message = t.DictType(t.StringType(), required=True)
    status_code = t.IntType(default=400, choices=[400, 401, 403, 404]) # Status codes include Bad Request, Unauthorized, Forbidden, and Not Found
    format_args = t.ListType(t.StringType(), default=[])
    include_payload = t.BooleanType(default=True)
    
    class Options:
        roles = {
            'public': whitelist('error_code', 'message', 'status_code')
        }

    def format_message(self, *args):
        self.format_args = args
        return self

class ErrorManager():

    def __init__(self):
        self.__errors = {}

    def get(self, name: str, default = None):
        try:
            return self.__errors[name]
        except KeyError:
            return default

    def add(self, error: Error):
        try:
            self.__errors[Error.error_name] = Error
            setattr(self, error.error_name, error)
        except:
            return

class AppError(Exception):

    def __init__(self, error: Error, lang: str = 'en_US'):
        super().__init__(self)
        self.error_code = error.error_code
        self.message = error.message[lang]
        if error.format_args:
            self.message = self.message.format(*error.format_args)
        self.status_code = error.status_code

    def to_dict(self):
        return dict(error_code=self.error_code, message=self.message)

INVALID_REQUEST_DATA = Error(dict(
    error_code='000000001',
    error_name='INVALID_REQUEST_DATA',
    message=dict(
        en_US='Invalid request contains the following errors: {}'
    )
))

ENDPOINT_NOT_FOUND = Error(dict(
    error_code='000000002', 
    error_name='ENDPOINT_NOT_FOUND',
    message=dict(
        en_US='Unable to find the requested endpoint. Subdomain: \'{}\', Module: \'{}\''
    ), 
    status_code=404
))
"""

CORE_EVENTS_CONTENT = """
from schematics import types as t, Model
"""

CORE_ROUTING_CONTENT = """
from schematics import Model
from schematics.exceptions import DataError

from . import activity
from .config import EndpointConfig
from .error import *

HEADERS_MAPPINGS_PATH = 'app.core.mappings.headers'
DATA_MAPPINGS_PATH = 'app.core.mappings.data'
SERVICES_MAPPINGS_PATH = 'app.core.mappings.services'

class MessageContext():

    def __init__(self):
        self.headers = {}
        self.data = None
        self.services = None
        self.result = {}
        self.errors = ErrorManager()


class FeatureHandler():
    def __init__(self, endpoint):
        if isinstance(endpoint, EndpointConfig):
            self.endpoint = endpoint
        elif isinstance(endpoint, dict):
            self.endpoint = EndpointConfig(endpoint)
        self.current_step = 0

    
    def handle(self, request, app_context, **kwargs):
        from time import time
        from importlib import import_module

        # Pull settings first.
        debug = kwargs.get('debug', False)

        # Create message context.
        context = MessageContext()

        # Add errors first.  It's easier this way...
        context.errors = app_context.errors

        # Begin header mapping process.
        if debug: print('Perform header mapping: "mapping": "{}"'.format(self.endpoint.header_mapping))

        # Import header mappings module.
        header_module = import_module(HEADERS_MAPPINGS_PATH)
        
        try:
            # Retrieve header mapping function.
            header_mapping_func = getattr(header_module, self.endpoint.header_mapping) 
        except TypeError:
            # Retrieve default header mapping function if none is specified.
            header_mapping_func = getattr(header_module, 'default')

        # Get header data and add to message context.
        context.headers = header_mapping_func(request, app_context, **kwargs)

        for module in self.endpoint.modules:
            
            # Map incoming message to headers, data, and services.
            if debug: print('Executing module: "module": "{}"'.format(module.to_primitive()))

            # Add current module to headers.
            context.headers['subdomain'] = module.subdomain
            context.headers['module'] = module.module

            context.headers['request_start'] = int(time())

            # Set data mapping and service container for endpoint module
            try:
                if module.data_mapping:
                    if debug: print('Perform data mapping: "mapping": "{}"'.format(module.data_mapping))
                    data_mapping = getattr(import_module(DATA_MAPPINGS_PATH), module.data_mapping)
                    context.data = data_mapping(context, request, app_context, **module.params, **kwargs)
                    if debug: print('Data mapping complete: "mapping": "{}", "data": "{}"'.format(module.data_mapping, context.data.to_primitive()))
                # Request model state validation
                try:
                    context.data.validate()
                except AttributeError: # In the case where there is no configured data mapping
                    pass
            except TypeError as ex:
                print(ex)
            except DataError as ex:
                print(ex)
                raise AppError(INVALID_REQUEST_DATA.format_message(ex.messages))
            try:
                use_services = getattr(import_module(SERVICES_MAPPINGS_PATH), module.use_services)
                context.services = use_services(context, request, app_context, **module.params)
            except TypeError:
                context.services = app_context.container

            # Retrieve module handler
            module_path = 'app.modules.{}.{}'.format(module.subdomain, module.module)
            try:
                handler = import_module(module_path)
            except ModuleNotFoundError as ex:
                raise AppError(ENDPOINT_NOT_FOUND.format_message(module.subdomain, module.module))

            # Execute handler function
            if debug: print('Executing module: {}.{}'.format(module.subdomain, module.module))
            result = handler.handle(context)
            # For those who do now wish to assign the results to the context in the handler
            if result:
                context.result = result

            # Log activity
            if module.log_activity:
                if debug: print('Logging activity for module: {}.{}'.format(module.subdomain, module.module))
                activity.handle(context)

            if debug: print('Finishing module: {}.{}'.format(module.subdomain, module.module))
        
        context.headers['request_end'] = int(time())

        # Return result
        # Handle list scenario
        if type(context.result) == list:
            result = []
            for item in context.result:
                if isinstance(item, Model):
                    result.append(item.to_primitive())
                else:
                    result.append(item)
            return result
        if not context.result:
            return {}
        # Convert schematics models to primitive dicts.
        if isinstance(context.result, Model):
            return context.result.to_primitive()
        return context.result
"""