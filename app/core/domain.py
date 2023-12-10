from typing import List, Any
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

class AppDomainModel(Model):
    pass


class ValueObject(AppDomainModel):
    pass


class Entity(AppDomainModel):

    id = t.StringType(required=True)