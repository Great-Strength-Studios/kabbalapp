from .value_objects import *
from .entities import *
from .modules import *

def create_type_properties(type: str, **properties)-> TypeProperties:
    if type == 'str':
        return StringTypeProperties.create(**properties)
    
    return None