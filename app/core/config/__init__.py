from schematics import types as t, Model

class AppConfiguration(Model):

    def __init__(self, name: str, **kwargs):
        self.name = name
        super().__init__(**kwargs)

    name = t.StringType(required=True)

    # endpoints: Dict[str, EndpointConfig] = {}
    # errors: Dict[str, Error] = {}

    # def __init__(self, 
    #     endpoints: Dict[str, EndpointConfig] = {}, 
    #     errors: Dict[str, Error] = {}): 

    #     self.endpoints = endpoints
    #     self.errors = errors


class AppConfigurationReader():

    def __init__(self, app_config_filepath: str):
        self.app_config_filepath = app_config_filepath

    def load_config(self, app_name: str, **kwargs) -> AppConfiguration:
        app_name, kwargs
        pass 