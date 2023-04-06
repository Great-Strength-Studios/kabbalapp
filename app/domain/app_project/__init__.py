from schematics import types as t, Model

class AppProject(Model):

    name = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    

class AppProjectManager():

    def __init__(self, app_project_filepath: str):
        self.app_project_filepath = app_project_filepath

    def load_project(self, app_key: str) -> AppProject:
        app_key
        pass

    def save_project(self, app_project: AppProject):
        app_project
        pass