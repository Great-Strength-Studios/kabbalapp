from .models import *
from .modules import *

def create_type_properties(type: str, **properties)-> TypeProperties:
    if type == STR_TYPE:
        return StringTypeProperties.create(**properties)
    elif type == LIST_TYPE:
        return ListTypeProperties.create(**properties)
    elif type == DATE_TYPE:
        return DateTypeProperties.create(**properties)
    elif type == DATETIME_TYPE:
        return DateTimeTypeProperties.create(**properties)
    
    return None