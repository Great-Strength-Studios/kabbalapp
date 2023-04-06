from schematics import types as t, Model

class AppProject(Model):

    name = t.StringType(required=True)
    app_directory = t.StringType(required=True)
    