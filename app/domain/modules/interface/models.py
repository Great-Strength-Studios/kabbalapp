from .. import *

class AppInterfaceType(ValueObject):
    name = t.StringType(required=True)
    type = t.StringType(required=True)
