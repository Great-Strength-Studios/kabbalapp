from typing import List
from schematics import types as t, Model

class AppProject(Model):

    name = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    schema_storage_type = t.StringType(choices=['yaml'], default='yaml')
    schema_location = t.StringType(required=True, default='app/schema.yaml')
    version = t.StringType(required=True, default='0.0.1')