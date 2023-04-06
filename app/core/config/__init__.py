import os
from schematics import types as t, Model

class AppConfiguration(Model):

    class ModuleConfiguration(Model):

        class FeatureConfiguration(Model):
            
            def __init__(self, raw_data: dict = None):
            # Account for single-module configuration
                try:
                    config = {}
                    config['modules'] = [{
                        'module_path': raw_data.pop('module_path'),
                        'params': raw_data.pop('params', {}),
                        'data_mapping': raw_data.pop('data_mapping', None),
                        'use_services': raw_data.pop('use_services', None),
                        'log_activity': raw_data.pop('log_activity', True)
                    }]
                    config['header_mapping'] = raw_data.pop('header_mapping', None)
                    super().__init__(raw_data=config)
                except KeyError:
                    super().__init__(raw_data=raw_data)

            class FunctionConfiguration(Model): 
                module_path = t.StringType(required=True)
                data_mapping = t.StringType()
                use_services = t.StringType()
                params = t.DictType(t.StringType(), default={})
                log_activity = t.BooleanType(default=True)


            header_mapping = t.StringType()
            functions = t.ListType(t.ModelType(FunctionConfiguration), default=[])
            log_params = t.DictType(t.StringType(), default={})


        features = t.DictType(FeatureConfiguration, default={})

    errors = t.DictType(t.StringType, default={}, serialize_when_none=False)
    modules = t.DictType(ModuleConfiguration, default={}, serialize_when_none=False)

class AppConfigurationReader():

    def __init__(self, app_config_filepath: str):
        self.app_config_filepath = app_config_filepath

    def load_config(self, app_name: str, **kwargs) -> AppConfiguration:
        app_name, kwargs
        pass 

def load_app_config_reader(app_config_filepath: str) -> AppConfigurationReader:
    if os.path.splitext(app_config_filepath)[1] in ['.yaml', '.yml']:
        from .yaml import YamlAppConfigurationReader
        return YamlAppConfigurationReader(app_config_filepath)
    elif os.path.splitext(app_config_filepath)[1] == '.json':
        from .json import JsonConfigurationReader
        return JsonConfigurationReader(app_config_filepath)