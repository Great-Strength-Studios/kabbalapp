from schematics import types as t, Model

from ...constants import *

class Domain(Model):
    key = t.StringType()
    name = t.StringType(required=True)

class DomainModel(Model):
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)

class DomainRole(Model):
    type = t.StringType(required=True, choices=DOMAIN_ROLE_TYPES)
    fields = t.ListType(t.StringType(), required=True)

class DomainService():

    def add_domain(self, domain_key: str, domain_name: str) -> Domain:
        pass

    def get_domain(self, domain_key: str) -> Domain:
        pass

    def add_domain_model(self, domain_key: str, model_key: str, model_name: str, class_name: str) -> DomainModel:
        pass