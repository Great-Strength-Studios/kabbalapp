from schematics import types as t, Model

class Domain(Model):
    key = t.StringType()
    name = t.StringType(required=True)

class DomainModel(Model):
    name = t.StringType(required=True)