from .models import *

class AppDomainService():

    def add_domain(self, domain_key: str, domain_name: str) -> AppDomain:
        pass

    def get_domain(self, domain_key: str) -> AppDomain:
        pass

    def add_domain_model(self, domain_key: str, model_key: str, model_name: str, class_name: str) -> AppDomainModel:
        pass

    def add_domain_role(self, domain_key: str, role_key: str, role_type: str, role_fields: List[str]) -> AppDomainRole:
        pass