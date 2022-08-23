import sys
from termios import ECHOE
import yaml
from typing import List
from functools import wraps

from schematics import Model, types as t
from schematics.exceptions import DataError

SERVICES_FILE = 'app/services/services.yml'



class ServiceParameter(Model):
    name = t.StringType(required=True)
    type = t.StringType(required=True)
    required = t.BooleanType(default=False, serialize_when_none=False)
    default = t.StringType(default=None, serialize_when_none=False)

class ServiceMethod(Model):
    name = t.StringType(required=True)
    params = t.ListType(t.ModelType(ServiceParameter), default=[], serialize_when_none=False)
    returns = t.StringType(default=None)

    def add_parameter(self, name: str, type: str, required: bool = False, default: str = None):
        param = ServiceParameter({
            'name': name,
            'type': type
        })
        if required:
            param.required = required
        if default:
            param.default = default

        try:
            self.params.append(param)
        except AttributeError:
            self.params = [param]
        
        return param

class ServiceModel(Model):
    name = t.StringType(required=True)
    type = t.StringType(choices=['Model', 'Enum', 'MondayModel'], default='Model')

class ServiceConfiguration(Model):
    name = t.StringType(required=True)
    type = t.StringType(choices=['default', 'inteface'], default='default')
    module = t.StringType(required=True)
    models = t.ListType(t.ModelType(ServiceModel), default=[], serialize_when_none=False)
    init_params = t.ListType(t.ModelType(ServiceParameter, default=[]), serialize_when_none=False)
    methods = t.ListType(t.ModelType(ServiceMethod), default=[], serialize_when_none=False)

    def add_parameter(self, name: str, type: str, required: bool = False, default: str = None):
        param = ServiceParameter({
            'name': name,
            'type': type
        })
        if required:
            param.required = required
        if default:
            param.default = default

        try:
            self.init_params.append(param)
        except AttributeError:
            self.init_params = [param]
        
        return param

    def get_method(self, method_id):
        try:
            return [method for method in self.methods if method.name == method_id][0]
        except IndexError:
            return None

    def add_method(self, name: str, params: List[ServiceParameter] = [], returns: str = None):
        method = ServiceMethod({
            'name': name,
        })
        if params:
            method.params = params
        if returns:
            method.returns = returns
        
        try:
            self.methods.append(method)
        except AttributeError:
            self.methods = [method]

        return method

    def add_model(self, name: str, type: str = 'Model'):
        model = ServiceModel({
            'name': name,
            'type': type
        })

        try:
            self.models.append(model)
        except AttributeError:
            self.models = [model]


class InterfaceServiceConfiguration(ServiceConfiguration):
    implementations = t.ListType(t.ModelType(ServiceConfiguration))

    def add_implementation(self, name: str, module: str, init_params: List[ServiceParameter] = []):
        impl = ServiceConfiguration({
            'name': name,
            'module': module
        })
        impl.init_params = [ServiceParameter(param) for param in init_params]

        try:
            self.implementations.append(impl)
        except AttributeError:
            self.implementations = [impl]
        
        return impl

def get_service_configs():
    with open(SERVICES_FILE, 'r') as stream:
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
    with open(SERVICES_FILE, 'w') as stream:
        config_data = [config.to_primitive() for config in configs]
        yaml.safe_dump(config_data, stream)

def get_service_config(service_configs: List[ServiceConfiguration], service_id: str, type: str = 'default'):
    try:
        service = [config for config in service_configs if config.name == service_id][0]
        return service
    except IndexError:
        None



def add_parameter(service_id, method_id, param_name, param_type, required = False, default = None):

    service_configs = get_service_configs()
    
    service_config = get_service_config(service_configs, service_id)
    if not service_config:
        print('Service not found: "{}"'.format(service_id))
    
    method_config = service_config.get_method(method_id)
    if not method_config:
        print('Service method not found: "{}"'.format(method_id))

    parameter = ServiceParameter({
        'name': param_name,
        'type': param_type
    })
    if required:
        parameter.required = required
    if default:
        parameter.default = str(default)
    
    try:
        method_config.params.append(parameter)
    except AttributeError:
        method_config.params = [parameter]

    save_service_configs(service_configs)

def new_service(name: str, type: str, module: str):
    service = ServiceConfiguration({
        'name': name,
        'type': type,
        'module': module
    })
    if type == 'interface':
        service = InterfaceServiceConfiguration(service.to_primitive())

    return service

def add_init_parameter(service_id, param_name: str, param_type: str, required: bool = False, default: str = None):
    service_configs = get_service_configs()
    service = get_service_config(service_configs, service_id)
    parameter = ServiceParameter({
        'name': param_name,
        'type': param_type,
    })
    if required:
        parameter.required = True
    if default:
        parameter.default = default
    
    try:
        service.init_params.append(parameter)
    except AttributeError:
        service.init_params = [parameter]

def add_model(service_id, name, type = 'Model'):
    service_configs = get_service_configs()
    service = get_service_config(service_configs, service_id)
    model = ServiceModel({
        'name': name,
        'type': type
    })

    try:
        service.models.append(model)
    except AttributeError:
        service.models = [model]

    save_service_configs(service_configs)

service_name = 'IdGeneratorService'

def execute(func):
    @wraps(func)

    def wrapper(*args, **kwargs):
        services = get_service_configs()
        func(services, *args, **kwargs)
        save_service_configs(services)
    return wrapper

@execute
def custom_workflow(services, *args, **kwargs):
    service: InterfaceServiceConfiguration = new_service('KeyService', 'interface', 'keys')
    method = service.add_method('get_key', returns='str')
    method.add_parameter('key', 'str', required=True)
    impl = service.add_implementation('AwsKeyService', 'secrets_manager')
    impl.add_parameter('region', 'str', default='us-east-1')
    services.append(service)


custom_workflow()

