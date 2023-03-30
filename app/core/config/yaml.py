import yaml

from . import *

class YamlAppConfigurationReader(AppConfigurationReader):

    def __init__(self, app_config_filepath: str):
        super().__init__(app_config_filepath)

    def load_config(self, app_name: str, **kwargs) -> AppConfiguration:
        with open(self.app_config_filepath) as stream:
            app_components = yaml.safe_load(stream)
        return AppConfiguration(app_name, **app_components[app_name], **kwargs)