from schematics import types as t, Model

class RequestEvent(Model):
    pass

class NewAppProject(RequestEvent):
    name = t.StringType(required=True)
    app_key = t.StringType(required=True)
    app_directory = t.StringType(required=True)