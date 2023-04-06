import os
from schematics import types as t, Model

class AppConfiguration(Model):

    endpoints = t.DictType(t.StringType(), t.DictType(t.StringType(), t.StringType()))
    errors = t.DictType(t.StringType(), t.DictType(t.StringType(), t.StringType()))
    mappings = t.DictType(t.StringType(), t.DictType(t.StringType(), t.StringType()))
    modules = t.DictType(t.StringType(), t.DictType(t.StringType(), t.StringType()))
    services = t.DictType(t.StringType(), t.DictType(t.StringType(), t.StringType()))


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