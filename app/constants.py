
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
    from .core import ContainerConfig

    container_config = ContainerConfig()
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
    container_config: ContainerConfig = None
    container: Container = None
    errors: ErrorManager = ErrorManager()
    endpoints: dict = None
    
    def __init__(self, name: str, app_config: AppConfig, container_config: ContainerConfig):
        self.name = name
        self._load_errors(app_config)
        self._load_endpoints(app_config)
        self._load_container(container_config)

    def _load_errors(self, app_config: AppConfig) -> None:
        for error in app_config.errors.values():
            self.errors.add(error)

    def _load_endpoints(self, app_config: AppConfig) -> None:
        self.endpoints = app_config.endpoints

    def _load_container(self, container_config: ContainerConfig) -> None:
        self.container_config = container_config
        self.container = Container(container_config)

    def run(self, **kwargs):
        pass


class AppBuilder():

    class Session():
        name: str = None
        app_config: AppConfig = None
        container_config: ContainerConfig = None

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

    def set_container_config(self, container_config: ContainerConfig):
        self._current_session.container_config = container_config
        return self

    def build(self):
        pass
"""

CORE_CONTAINER_CONTENT = """
from schematics import types as t, Model

from ..services import SkyWellness, ConfigurationService

# Container configuration
class ContainerConfig(Model):
    pass


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfig):
        # Default init
        self.config = config

        # Custom init below
        # ...

    def config_service(self) -> ConfigurationService:
        from ..services.config.yaml import YamlConfigurationService

        return YamlConfigurationService('config.yml')


    def skywellness(self, profile_name=None) -> SkyWellness:
        from ..services.skywellness.salesforce import SkyWellnessSalesforce

        config_service = self.config_service()
        if not profile_name:
            profile_name = config_service.config.default_profile
        profile = self.config_service.get_profile(profile_name)
        
        return SkyWellnessSalesforce(
            profile.username, 
            profile.password, 
            profile.security_token, 
            profile.is_sandbox)
    

# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)
"""