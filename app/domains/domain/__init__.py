from schematics import types as t, Model

### Section - Domain Models ###
class Domain(Model):
    name = t.StringType(required=True)


### Section - Domain Entities ###
class DomainEntity(Domain):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)