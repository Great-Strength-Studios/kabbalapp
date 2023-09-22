from ..entities import *

class AppInterface(Model):
    type = t.StringType(required=True, choices=['cli', 'rest_flask'])
    mappers = t.DictType(t.StringType())
