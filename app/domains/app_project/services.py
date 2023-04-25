from .models import *

class AppProjectManager():

    def load_project(self, key: str = None) -> AppProject:
        pass

    def save_project(self, key: str, app_project: AppProject):
        pass

    def set_default_app_project(self, key: str):
        pass
