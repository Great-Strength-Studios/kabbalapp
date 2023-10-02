from .models import *
from .modules import *

def create_type_properties(type: str, **properties)-> TypeProperties:
    if type == 'str':
        return StringTypeProperties.create(**properties)
    elif type == 'list':
        return ListTypeProperties.create(**properties)
    
    return None