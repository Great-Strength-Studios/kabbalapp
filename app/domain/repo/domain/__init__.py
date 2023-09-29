from ...entities import *
from ...modules import *

class DomainRepository():

    # TODO: Incorporate real domain model later.
    def get_domain_model(self, id: str) -> ValueObject:
        pass

    def get_value_objects(self) -> List[ValueObject]:
        pass

    def save_value_object(self, value_object: ValueObject) -> None:
        pass