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
        self.name = name
        self._load_errors(app_config)
        self._load_endpoints(app_config)
        self._load_container(container_config)

    def _load_errors(self, app_config: AppConfiguration) -> None:
        for error in app_config.errors.values():
            self.errors.add(error)

    def _load_endpoints(self, app_config: AppConfiguration) -> None:
        self.endpoints = app_config.endpoints

    def _load_container(self, container_config: ContainerConfig) -> None:
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
        app_config = app_config_reader.load_config()
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