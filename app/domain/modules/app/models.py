from ...models import *

class AppProject(Entity):
    tag = t.StringType(required=True)
    name = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    schema_storage_type = t.StringType(choices=['yaml'], default='yaml')
    schema_location = t.StringType(required=True, default='app/app.yml')
    version = t.StringType(required=True)

    @staticmethod
    def create(name: str, tag: str, app_directory: str, schema_storage_type: str = 'yaml', schema_location: str = 'app/app.yml', version: str = '0.0.1'):
        app_project = AppProject()
        app_project.name = name
        app_project.tag = tag
        app_project.id = tag
        app_project.app_directory = app_directory
        app_project.schema_storage_type = schema_storage_type
        app_project.schema_location = schema_location
        app_project.version = version

        app_project.validate()
        return app_project