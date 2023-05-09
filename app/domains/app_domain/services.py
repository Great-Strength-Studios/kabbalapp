from .models import *

class AppDomainService():

    def add_domain(self, key: str, name: str, aliases: List[str]) -> AppDomain:
        pass

    def get_domain(self, key: str) -> AppDomain:
        pass

    def update_domain(self, key: str, name: str, aliases: List[str]) -> AppDomain:
        pass 

    def add_implementation(self, domain_key: str, name: str, key: str) -> AppDomainImplementation:
        pass

    def get_implementation(self, domain_key: str, implementation_key: str) -> AppDomainImplementation:
        pass

    def add_model(self, domain_key: str, key: str, name: str, class_name: str) -> AppDomainModel:
        pass

    def get_model(self, domain_key: str, key: str) -> AppDomainModel:
        pass

    def add_role(self, domain_key: str, key: str, type: str, fields: List[str]) -> AppDomainRole:
        pass

    def add_property(self, domain_key: str, model_key: str, key: str, name: str,  type: str, **kwargs) -> AppDomainModelProperty:
        pass