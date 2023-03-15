from typing import Dict

from .error import *
from .containers import *
from .routing import *
from .events import *

class AppConfig():

    endpoints: Dict[str, EndpointConfig] = {}
    errors: Dict[str, Error] = {}

    def __init__(self, 
        endpoints: Dict[str, EndpointConfig] = {}, 
        errors: Dict[str, Error] = {}): 

        self.endpoints = endpoints
        self.errors = errors


class AppContext():

    name: str = None
    container_config: ContainerConfig = None
    container: Container = None
    errors: ErrorManager = ErrorManager()
    endpoints: dict = None
    
    def __init__(self, name: str, app_config: AppConfig, container_config: ContainerConfig):
        self.name = name
        self._load_errors(app_config)
        self._load_endpoints(app_config)
        self._load_container(container_config)

    def _load_errors(self, app_config: AppConfig) -> None:
        for error in app_config.errors.values():
            self.errors.add(error)

    def _load_endpoints(self, app_config: AppConfig) -> None:
        self.endpoints = app_config.endpoints

    def _load_container(self, container_config: ContainerConfig) -> None:
        self.container_config = container_config
        self.container = Container(container_config)

    def run(self, **kwargs):
        pass


class AppBuilder():

    class Session():
        name: str = None
        app_config: AppConfig = None
        container_config: ContainerConfig = None

    _current_session = None

    @property
    def app_config(self) -> AppConfig:
        return self._current_session.app_config

    def create_new_app(self, name: str, **kwargs):
        kwargs
        if self._current_session:
            self._current_session = None
        self._current_session = self.Session()
        self._current_session.name = name
        return self

    def set_app_config(self, app_config: AppConfig):
        self._current_session.app_config = app_config
        return self

    def set_container_config(self, container_config: ContainerConfig):
        self._current_session.container_config = container_config
        return self

    def build(self):
        pass