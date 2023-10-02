from typing import List, Any
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

class DomainModel(Model):
    pass


class ValueObject(DomainModel):
    pass


class Entity(DomainModel):

    id = t.StringType(required=True)