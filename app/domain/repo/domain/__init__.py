from ...models import *
from ...modules import *

class DomainRepository():

    # TODO: Incorporate real domain model later.
    def get_domain_model(self, id: str) -> AppDomainModel:
        pass

    def get_domain_models(self, type: str = None) -> List[AppDomainModel]:
        pass

    def save_domain_model(self, domain_model: AppDomainModel) -> None:
        pass