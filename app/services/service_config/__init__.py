from typing import List

from schematics import Model, types as t

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