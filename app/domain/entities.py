from .value_objects import *

class ValueObject(Model):
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    class_name = t.StringType(required=True)
    properties = t.ListType(t.ModelType(DomainModelProperty), default=[])

    @staticmethod
    def create(name: str, class_name: str, id: str = None, properties: List[DomainModelProperty] = []) -> 'ValueObject':
        result = ValueObject()
        result.name = name
        result.class_name = class_name
        result.properties = properties

        # Convert python camel case to snake case if ID is not provided
        if id is None:
            import re
            result.id = name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        else:
            result.id = id

        result.validate()

        return result
    
    def has_property(self, property: DomainModelProperty) -> bool:
        return any((p.name == property.name for p in self.properties))

    def add_property(self, property: DomainModelProperty) -> None:
        self.properties.append(property)

class TypeProperties(Model):
    pass

class StringTypeProperties(TypeProperties):
    regex = t.StringType()
    min_length = t.IntType()
    max_length = t.IntType()

class DateTypeProperties(TypeProperties):
    formats = t.StringType()

class DateTimeTypeProperties(TypeProperties):
    formats = t.StringType()
    serialized_format = t.StringType()
    parser = t.StringType()
    tzd = t.StringType(default='allow', choices=['require', 'allow', 'utc', 'reject'])
    convert_tz = t.BooleanType(default=False)
    drop_tzinfo = t.BooleanType(default=False)