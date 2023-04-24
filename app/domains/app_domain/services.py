from .models import *

class AppDomainService():

    def add_domain(self, key: str, name: str, aliases: List[str]) -> AppDomain:
        pass

    def get_domain(self, key: str) -> AppDomain:
        pass

    def add_model(self, domain_key: str, key: str, name: str, class_name: str) -> AppDomainModel:
        pass

    def add_role(self, domain_key: str, key: str, type: str, fields: List[str]) -> AppDomainRole:
        pass

    def add_property(self, domain_key: str, model_key: str, key: str, name: str,  type: str, metadata: dict) -> AppDomainModelProperty:
        pass