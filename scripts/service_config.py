import os
import yaml
from typing import List
from functools import wraps

from schematics.exceptions import DataError

import sys
sys.path.append(os.getcwd())


from app.domain.service_config import ServiceConfiguration, InterfaceServiceConfiguration

APP_FILE_PATH = '/Users/ashatz/Work/Code/entman-webhooks-api'
SERVICES_FILE = 'app/services/services.yml'

def get_service_configs():
    with open(os.path.join(APP_FILE_PATH, SERVICES_FILE), 'r') as stream:
        config_file = yaml.safe_load(stream)

        service_configs = []
        for service_config in config_file:
            try:
                service = ServiceConfiguration(service_config)
                if service.type == 'interface':
                    service = InterfaceServiceConfiguration(service_config)
            except DataError as ex:
                try:
                    ex.errors['implementations']
                    service = InterfaceServiceConfiguration(service_config)
                except KeyError as ex:
                    continue
            service_configs.append(service)
    return service_configs

def save_service_configs(configs: List[ServiceConfiguration]):
    with open(os.path.join(APP_FILE_PATH, SERVICES_FILE), 'w') as stream:
        config_data = [config.to_primitive() for config in configs]
        yaml.safe_dump(config_data, stream)

def get_service_config(service_configs: List[ServiceConfiguration], service_id: str, type: str = 'default'):
    try:
        service = [config for config in service_configs if config.name == service_id][0]
        return service
    except IndexError:
        None

def new_service(name: str, type: str, module: str):
    service = ServiceConfiguration({
        'name': name,
        'type': type,
        'module': module
    })
    if type == 'interface':
        service = InterfaceServiceConfiguration(service.to_primitive())

    return service


def execute(func):
    @wraps(func)

    def wrapper(*args, **kwargs):
        services = get_service_configs()
        func(services, *args, **kwargs)
        save_service_configs(services)
    return wrapper

@execute
def custom_workflow(services, *args, **kwargs):
    # Add custom code here.
    pass

custom_workflow()