from typing import Dict

from ..constants import APP_CONFIGURATION_FILE
from .config import load_app_config_reader, AppConfigurationReader, AppConfiguration
from .error import *
from .containers import *
from .routing import *
from .events import *


class AppContext():

    name: str = None
    container_config: ContainerConfig = None
    container: Container = None
    errors: ErrorManager = ErrorManager()
    endpoints: dict = None
    
    def __init__(self, name: str, app_config: AppConfiguration, container_config: ContainerConfig):
        # Set app name.
        self.name = name
        
        # Load app errors.
        try:
            for error in app_config.errors.values():
                self.errors.add(error)
        except AttributeError:
            pass

        self.endpoints = app_config.endpoints

        # Load container config and container.
        self.container_config = container_config
        self.container = Container(container_config)


    def run(self, **kwargs):
        pass


class AppBuilder():

    class Session():
        def __init__(self, name: str, app_config: AppConfiguration, container_config: ContainerConfig):
            self.name = name
            self.app_config = app_config
            self.container_config = container_config

    _current_session = None

    @property
    def app_config(self) -> AppConfiguration:
        return self._current_session.app_config

    def create_new_app(self, name: str, config_file: str = APP_CONFIGURATION_FILE, **kwargs):
        kwargs
        if self._current_session:
            self._current_session = None
        app_config_reader: AppConfigurationReader = load_app_config_reader(config_file)
        app_config = app_config_reader.load_config(strict=False)
        self._current_session = self.Session(
            name=name,
            app_config=app_config,
            container_config=None
        )
        return self

    def set_app_config(self, app_config: AppConfiguration):
        self._current_session.app_config = app_config
        return self

    def set_container_config(self, container_config: ContainerConfig):
        self._current_session.container_config = container_config
        return self

    def build(self):
        pass