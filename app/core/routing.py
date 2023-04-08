from schematics import types as t, Model
from schematics.exceptions import DataError

from . import activity
from ..core.config import FeatureConfiguration
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
    def __init__(self, feature_config):
        if isinstance(feature_config, FeatureConfiguration):
            self.feature_config = feature_config
        elif isinstance(feature_config, dict):
            self.feature_config = FeatureConfiguration(feature_config)
        self.current_step = 0

    
    def handle(self, context: MessageContext, request, app_context, **kwargs):
        from time import time
        from importlib import import_module

        # Pull settings first.
        debug = kwargs.get('debug', False)

        # Add errors first.  It's easier this way...
        context.errors = app_context.errors

        # Begin header mapping process.
        if debug: print('Perform header mapping: "mapping": "{}"'.format(self.feature_config.header_mapping))

        # Import header mappings module.
        header_module = import_module(HEADERS_MAPPINGS_PATH)
        
        try:
            # Retrieve header mapping function.
            header_mapping_func = getattr(header_module, self.feature_config.header_mapping) 
        except TypeError:
            # Retrieve default header mapping function if none is specified.
            header_mapping_func = getattr(header_module, 'default')

        # Get header data and add to message context.
        context.headers = header_mapping_func(request, app_context, **kwargs)

        for function in self.feature_config.functions:

            if debug: print('Executing function: "function": "{}"'.format(function.to_primitive()))

            context.headers['request_start'] = int(time())

            # Set data mapping and service container for feature function
            try:
                if function.data_mapping:
                    if debug: print('Perform data mapping: "mapping": "{}"'.format(function.data_mapping))
                    data_mapping = getattr(import_module(DATA_MAPPINGS_PATH), function.data_mapping)
                    context.data = data_mapping(context, request, app_context, **function.params, **kwargs)
                    if debug: print('Data mapping complete: "mapping": "{}", "data": "{}"'.format(function.data_mapping, context.data.to_primitive()))
                # Request model state validation
                try:
                    context.data.validate()
                except AttributeError: # In the case where there is no configured data mapping
                    pass
            except TypeError as ex:
                print(ex)
            except DataError as ex:
                print(ex)
                raise AppError(app_context.errors.INVALID_REQUEST_DATA.format_message(ex.messages))
            try:
                use_services = getattr(import_module(SERVICES_MAPPINGS_PATH), function.use_services)
                context.services = use_services(context, request, app_context, **function.params)
            except TypeError:
                context.services = app_context.container

            # Format function module path.
            module_path = 'app.modules.{}'.format(function.function_path)

            # Import function module.
            if debug: print('Importing function: {}'.format(module_path))
            handler = import_module(module_path)

            # Execute function handler.
            if debug: print('Executing function: {}'.format(module_path))
            result = handler.handle(context)
            # For those who do now wish to assign the results to the context in the handler
            if result:
                context.result = result

            # Log activity
            if function.log_activity:
                if debug: print('Logging activity for function: {}'.format(module_path))
                activity.handle(context)

            if debug: print('Finishing function: {}'.format(module_path))
        
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