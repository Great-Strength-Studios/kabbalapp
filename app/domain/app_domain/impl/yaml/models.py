from ...models import *

class YamlAppDomainModelProperty(AppDomainModelProperty):

    class Options():
        serialize_when_none = False,
        roles = {
            'domain.add_property': blacklist('key')
        }