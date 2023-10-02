from ..models import *

class AppInterfaceType(ValueObject):
    type = t.StringType(required=True)
    name = t.StringType(required=True)
