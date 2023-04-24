import os, yaml

from ..services import *

class YamlAppProjectManager(AppProjectManager):

    def __init__(self, app_project_filepath: str):
        self.app_project_filepath = app_project_filepath
        if not os.path.exists(self.app_project_filepath):
            os.makedirs(os.path.dirname(self.app_project_filepath), exist_ok=True)
            with open(self.app_project_filepath, 'w') as stream:
                stream.write('')

    def load_project(self, app_key: str) -> AppProject:
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        return AppProject(app_projects[app_key])

    def save_project(self, app_key: str, app_project: AppProject):
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        try:
            app_projects[app_key] = app_project.to_primitive()
        except TypeError:
            app_projects = {app_key: app_project.to_primitive()}
        with open(self.app_project_filepath, 'w') as stream:
            yaml.safe_dump(app_projects, stream)