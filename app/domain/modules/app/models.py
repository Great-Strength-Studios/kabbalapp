from ...models import *

class AppProject(Model):
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    schema_storage_type = t.StringType(choices=['yaml'], default='yaml')
    schema_location = t.StringType(required=True, default='app/app.yml')
    version = t.StringType(required=True)