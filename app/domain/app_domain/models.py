from typing import List
from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

from ...constants import *

class AppDomainModel(Model):
    key = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)

    class Options():
        serialize_when_none = False
        roles = {
            'domain.add_model': blacklist('key'),
            'domain.add_property': blacklist('key'),
            'domain.get_domain': blacklist(),
            'domain.list_domain_models': blacklist(),
        }

class AppDomainRole(Model):
    type = t.StringType(required=True)
    fields = t.ListType(t.StringType(), required=True)