from typing import List
from schematics import types as t, Model

from ...constants import *

class AppDomain(Model):
    key = t.StringType()
    name = t.StringType(required=True)

class AppDomainModel(Model):
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)

class AppDomainRole(Model):
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)