from .core import *

class DomainModelEntity(DomainModel):
    def __init__(self, domain_service: DomainService,  **kwargs):
        self.domain_service = domain_service
        super().__init__(**kwargs)

class DomainEntity(Domain):

    def __init__(self, domain_service: DomainService,  **kwargs):
        self.domain_service = domain_service
        super().__init__(**kwargs)

    def add_model(self, key: str, name: str) -> DomainModelEntity:
        model = self.domain_service.add_domain_model(self.key, key, name)
        return DomainModelEntity(domain_service=self.domain_service, raw_data=model.to_primitive())
    
def add_domain(domain_service: DomainService, domain_key: str, domain_name: str):
    domain = domain_service.add_domain(domain_key, domain_name)
    if isinstance(domain, tuple):
        return domain
    return DomainEntity(domain_service=domain_service, raw_data=domain.to_primitive())

def get_domain(domain_service: DomainService, domain_key: str):
    domain = domain_service.get_domain(domain_key)
    if isinstance(domain, tuple):
        return domain
    return DomainEntity(domain_service=domain_service, raw_data=domain.to_primitive())