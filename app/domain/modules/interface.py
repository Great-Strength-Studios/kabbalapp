from ..entities import *

class AppInterfaceType(Model):
    type = t.StringType(required=True)
    name = t.StringType(required=True)
