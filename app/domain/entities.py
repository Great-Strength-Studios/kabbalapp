from .value_objects import *

class ValueObject(Model):
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    properties = t.ListType(t.StringType(), default=[])

    @staticmethod
    def create(name: str, class_name: str, id: str = None) -> 'ValueObject':
        result = ValueObject()
        result.name = name
        result.class_name = class_name

        # Convert python camel case to snake case if ID is not provided
        if id is None:
            import re
            result.id = name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        else:
            result.id = id

        return result