from .models import *

class AppProjectManager():

    def load_project(self, app_key: str) -> AppProject:
        pass

    def save_project(self, app_key: str, app_project: AppProject):
        pass

    def set_default_app_project(self, app_key: str):
        pass