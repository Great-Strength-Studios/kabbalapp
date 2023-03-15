from schematics import types as t, Model

from ..services import SkyWellness, ConfigurationService

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

    def config_service(self) -> ConfigurationService:
        from ..services.config.yaml import YamlConfigurationService

        return YamlConfigurationService('config.yml')


    def skywellness(self, profile_name=None) -> SkyWellness:
        from ..services.skywellness.salesforce import SkyWellnessSalesforce

        config_service = self.config_service()
        if not profile_name:
            profile_name = config_service.config.default_profile
        profile = self.config_service.get_profile(profile_name)
        
        return SkyWellnessSalesforce(
            profile.username, 
            profile.password, 
            profile.security_token, 
            profile.is_sandbox)
    

# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)