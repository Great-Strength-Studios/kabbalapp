from ...models import *

class AppProject(Entity):
    app_directory = t.StringType(required=True)
    schema_storage_type = t.StringType(choices=['yaml'], default='yaml')
    schema_location = t.StringType(required=True, default='app/app.yml')
    version = t.StringType(required=True)

    @staticmethod
    def create(name: str, id: str, app_directory: str, schema_storage_type: str = 'yaml', schema_location: str = 'app/app.yml', version: str = '0.0.1'):
        # Create new app project instance.
        app_project = AppProject()

        # Add properties.
        app_project.id = id
        app_project.name = name
        app_project.app_directory = app_directory
        app_project.schema_storage_type = schema_storage_type
        app_project.schema_location = schema_location
        app_project.version = version

        # Validate.
        app_project.validate()

        # Return new app project instance.
        return app_project