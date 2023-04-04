from schematics import types as t, Model

# Container configuration
class ContainerConfig(Model):
    pass


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfig):
        # Default init
        self.config = config

        # Custom init below
        # ...
    

# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)