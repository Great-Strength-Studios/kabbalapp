from schematics import types as t, Model

# Container configuration
class ContainerConfiguration(Model):
    
    app_project_filepath = t.StringType(required=False, default=None)


# Default container
class Container():

    # Custom fields below
    # ...

    def __init__(self, config: ContainerConfiguration):
        # Default init
        self.config = config

        # Custom init below
        # ...
    def app_project_manager(self):
        import os
        if self.config.app_project_filepath and os.path.splitext(self.config.app_project_filepath)[1] in ['.yaml', '.yml']:
            from ..domain.app_project.impl import YamlAppProjectManager
            return YamlAppProjectManager(self.config.app_project_filepath)
        
    def app_printer(self, app_key: str = None):
        import os
        from ..domain.app_printer import AppPrinter
        if not app_key:
            return AppPrinter(os.getcwd())
        app_project_manager = self.app_project_manager()
        app_project = app_project_manager.load_project(app_key)
        return AppPrinter(app_project.app_directory)

    def domain_service(self, app_key: str):
        app_project_manager = self.app_project_manager()
        app_project = app_project_manager.load_project(app_key)
        if app_project.schema_storage_type == 'yaml':
            from ..domain.app_domain.impl import YamlAppDomainService
            return YamlAppDomainService(app_project.app_directory, app_project.schema_location)
        
    def interface_repo(self, app_key: str):
        app_project_manager = self.app_project_manager()
        app_project = app_project_manager.load_project(app_key)
        if app_project.schema_storage_type == 'yaml':
            from ..domain.modules.interface.repo.yaml import YamlRepository
            return YamlRepository(app_project.app_directory, app_project.schema_location)

    def cli_interface_repo(self, app_key: str):
        app_project_manager = self.app_project_manager()
        app_project = app_project_manager.load_project(app_key)
        if app_project.schema_storage_type == 'yaml':
            from ..domain.modules.cli.repo.yaml import YamlRepository
            return YamlRepository(app_project.app_directory, app_project.schema_location)
        
    def domain_repo(self, app_key: str):
        app_project_manager = self.app_project_manager()
        app_project = app_project_manager.load_project(app_key)
        if app_project.schema_storage_type == 'yaml':
            from ..domain.modules.domain.repo.yaml import YamlRepository
            return YamlRepository(app_project.app_directory, app_project.schema_location)


# Default dynamic container
class DynamicContainer():
    
    def add_service(self, service_name, factory_func):
        setattr(self, service_name, factory_func)