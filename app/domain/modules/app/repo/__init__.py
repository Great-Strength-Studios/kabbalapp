from ..models import *

class AppProjectRepository():

    def project_exists(self, tag: str) -> bool:
        pass

    def load_project(self, tag: str = None) -> AppProject:
        pass

    def save_project(self, app_project: AppProject) -> AppProject:
        pass

    def set_default_app_project(self, tag: str):
        pass