from ..models import *

class AppProjectRepository():

    def project_exists(self, id: str) -> bool:
        pass

    def load_project(self, id: str = None) -> AppProject:
        pass

    def save_project(self, app_project: AppProject) -> AppProject:
        pass

    def default_app_project_configured(self) -> bool:
        pass

    def set_default_app_project(self, id: str):
        pass