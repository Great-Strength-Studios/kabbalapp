from schematics import types as t, Model

### Section - Models ###
class Domain(Model):
    key = t.StringType()
    name = t.StringType(required=True)


### Section - Entities ###
class DomainEntity(Domain):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

### Section - Services ###
class DomainService():

    def add_domain(self, domain_key: str, domain_name: str) -> DomainEntity:
        pass