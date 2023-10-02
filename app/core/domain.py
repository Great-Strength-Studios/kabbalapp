from typing import List
from schematics import types as t, Model

class DomainModel(Model):

    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=['entity', 'value_object'])
    class_name = t.StringType(required=True)    


class ValueObject(DomainModel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'value_object'

class Entity(DomainModel):

    id = t.StringType(required=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'entity'