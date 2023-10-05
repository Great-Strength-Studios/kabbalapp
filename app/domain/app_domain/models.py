from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

from ...constants import *

class AppDomainRole(Model):
    type = t.StringType(required=True)
    fields = t.ListType(t.StringType(), required=True)