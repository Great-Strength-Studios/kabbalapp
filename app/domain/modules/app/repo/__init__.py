from ..models import *

class AppProjectRepository():

    def project_exists(self, key: str) -> bool:
        pass

    def load_project(self, key: str = None) -> AppProject:
        pass

    def save_project(self, app_project: AppProject) -> AppProject:
        pass

    def set_default_app_project(self, key: str):
        pass