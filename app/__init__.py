
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
