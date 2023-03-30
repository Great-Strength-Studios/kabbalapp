import json

from . import *

class JsonConfigurationReader(AppConfigurationReader):
    
    def load_config(self, app_name: str, **kwargs) -> AppConfiguration:
        with open(self.app_config_filepath) as stream:
            app_components = json.load(stream)
        return AppConfiguration(app_name, **app_components[app_name], **kwargs)