import yaml

from . import *

class AppProjectDataMapper(AppProject):

    class Options():
        roles = {
            'write': blacklist('id'),
            'map': blacklist(),
        }

class YamlRepository(AppProjectRepository):

    def __init__(self, app_project_filepath: str):
        import os
        self.app_project_filepath = app_project_filepath
        if not os.path.exists(self.app_project_filepath):
            os.makedirs(os.path.dirname(self.app_project_filepath), exist_ok=True)
            with open(self.app_project_filepath, 'w') as stream:
                data = {'projects': None, 'default_project': None}
                yaml.safe_dump(data, stream)

    def project_exists(self, id: str) -> bool:
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        return id in app_projects['projects']

    def load_project(self, id: str = None) -> AppProject:
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        # If no id is provided, return the default project.
        if id is None:
            id = app_projects['default_project']

        project = AppProject(app_projects['projects'][id])
        project.id = id
        return project

    def save_project(self, app_project: AppProject):
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        projects = app_projects.get('projects', {})
        mapper = AppProjectDataMapper(app_project.to_primitive())
        projects[app_project.id] = mapper.to_primitive('write')
        with open(self.app_project_filepath, 'w') as stream:
            yaml.safe_dump(app_projects, stream)

    def set_default_app_project(self, id: str):
        with open(self.app_project_filepath) as stream:
            app_projects = yaml.safe_load(stream)
        app_projects['default_project'] = id
        with open(self.app_project_filepath, 'w') as stream:
            yaml.safe_dump(app_projects, stream)