from .models import *

class AppDomainService():

    def add_model(self, domain_key: str, key: str, name: str, class_name: str) -> AppDomainModel:
        pass

    def get_models(self, domain_key: str = None) -> List[AppDomainModel]:
        pass

    def get_model(self, domain_key: str, key: str) -> AppDomainModel:
        pass

    def add_role(self, domain_key: str, key: str, type: str, fields: List[str]) -> AppDomainRole:
        pass