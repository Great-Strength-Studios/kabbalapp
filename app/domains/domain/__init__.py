from schematics import types as t, Model

class Domain(Model):
    name = t.StringType(required=True)