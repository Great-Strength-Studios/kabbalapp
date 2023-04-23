from typing import List
from schematics import types as t, Model

from ...constants import *

class AppDomainModel(Model):
    name = t.StringType(required=True)

class AppDomainRole(Model):
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class AppDomain(Model):
    key = t.StringType()
    name = t.StringType(required=True)
    roles = t.DictType(t.ModelType(AppDomainRole), default={})
    models = t.DictType(t.ModelType(AppDomainModel), default={})