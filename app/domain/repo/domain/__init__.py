from ...entities import *
from ...modules import *

class DomainRepository():

    # TODO: Incorporate real domain model later.
    def get_domain_model(self, id: str) -> AppValueObject:
        pass

    def get_value_objects(self) -> List[AppValueObject]:
        pass

    def save_value_object(self, value_object: AppValueObject) -> None:
        pass