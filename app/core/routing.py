from schematics import types as t, Model
from schematics.exceptions import DataError

from . import activity
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


class EndpointConfig(Model):

    def __init__(self, raw_data: dict = None):
        # Account for single-module configuration
        try:
            config = {}
            config['modules'] = [{
                'subdomain': raw_data.pop('subdomain'),
                'module': raw_data.pop('module'),
                'params': raw_data.pop('params', {}),
                'data_mapping': raw_data.pop('data_mapping', None),
                'use_services': raw_data.pop('use_services', None),
                'log_activity': raw_data.pop('log_activity', True)
            }]
            config['header_mapping'] = raw_data.pop('header_mapping', None)
            super().__init__(raw_data=config)
        except KeyError:
            super().__init__(raw_data=raw_data)

    class ModuleConfiguration(Model): 
        subdomain = t.StringType(required=True)
        module = t.StringType(required=True)
        data_mapping = t.StringType()
        use_services = t.StringType()
        params = t.DictType(t.StringType(), default={})
        log_activity = t.BooleanType(default=True)

    header_mapping = t.StringType()
    modules = t.ListType(t.ModelType(ModuleConfiguration), default=[])
    log_params = t.DictType(t.StringType(), default={})


class EndpointHandler():
    def __init__(self, endpoint):
        if isinstance(endpoint, EndpointConfig):
            self.endpoint = endpoint
        elif isinstance(endpoint, dict):
            self.endpoint = EndpointConfig(endpoint)
        self.current_step = 0

    
    def handle(self, context: MessageContext, request, app_context, **kwargs):
        from time import time
        from importlib import import_module

        # Pull settings first.
        debug = kwargs.get('debug', False)

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