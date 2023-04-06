import yaml

from . import *

class YamlAppProjectManager(AppProjectManager):

    def __init__(self, app_project_filepath: str):
        self.app_project_filepath = app_project_filepath

    def load_project(self, app_key: str) -> AppProject:
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        return AppProject(app_projects[app_key])

    def save_project(self, app_project: AppProject):
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        app_projects[app_project.name] = app_project.to_primitive()
        with open(self.app_project_filepath, 'w') as stream:
            yaml.safe_dump(app_projects, stream)