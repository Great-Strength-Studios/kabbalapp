import os, yaml

from ..services import *

class YamlAppProjectManager(AppProjectManager):

    def __init__(self, app_project_filepath: str):
        self.app_project_filepath = app_project_filepath
        if not os.path.exists(self.app_project_filepath):
            os.makedirs(os.path.dirname(self.app_project_filepath), exist_ok=True)
            with open(self.app_project_filepath, 'w') as stream:
                data = {'projects': None, 'default_project': None}
                yaml.safe_dump(data, stream)

    def load_project(self, key: str = None) -> AppProject:
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        # If no key is provided, return the default project.
        if key is None:
            key = app_projects['default_project']
        try:
            return AppProject(app_projects['projects'][key])
        except KeyError:
            return ('APP_PROJECT_NOT_FOUND', key)

    def save_project(self, key: str, app_project: AppProject):
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        try:
            app_projects['projects'][key] = app_project.to_primitive()
        except TypeError:
            app_projects['projects'] = {key: app_project.to_primitive()}
        with open(self.app_project_filepath, 'w') as stream:
            yaml.safe_dump(app_projects, stream)

    def set_default_app_project(self, key: str):
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        if key not in app_projects['projects']:
            return ('APP_PROJECT_NOT_FOUND', key)
        app_projects['default_project'] = key
        with open(self.app_project_filepath, 'w') as stream:
            yaml.safe_dump(app_projects, stream)