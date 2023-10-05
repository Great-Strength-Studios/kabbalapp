from ...models import *


class DomainModelProperty(ValueObject):

    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
    inner_type = t.StringType()
    required = t.BooleanType()
    default = t.StringType()
    choices = t.ListType(t.StringType())
    description = t.StringType()
    type_properties = t.ModelType(TypeProperties)

    @staticmethod
    def create(name: str, type: str = 'str', inner_type: str = None, required: bool = False, default: str = None, choices: List[str] = None, description: str = None, type_properties: TypeProperties = None) -> 'DomainModelProperty':
        result = DomainModelProperty()
        result.name = name
        result.type = type
        result.inner_type = inner_type
        result.required = required
        result.default = default
        result.choices = choices
        result.description = description
        result.type_properties = type_properties

        result.validate()
        
        return result


class AppDomainModel(Entity):
    test = t.StringType()
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_MODEL_TYPES)
    class_name = t.StringType(required=True)
    properties = t.ListType(t.ModelType(DomainModelProperty), default=[])

    @staticmethod
    def create(name: str, type: str, class_name: str, id: str = None, properties: List[DomainModelProperty] = []) -> 'AppDomainModel':
        result = AppDomainModel()
        result.name = name
        result.type = type
        result.class_name = class_name
        result.properties = properties

        # Convert python camel case to snake case if ID is not provided
        if id is None:
            import re
            result.id = name = re.sub(
            	r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        else:
            result.id = id

        result.validate()

        return result

    def has_property(self, property: DomainModelProperty) -> bool:
        return any((p.name == property.name for p in self.properties))

    def add_property(self, property: DomainModelProperty) -> None:
        self.properties.append(property)
