from ...models import *


class DomainModelProperty(ModelProperty):

    type = t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
    inner_type_model_id = t.StringType()

    @staticmethod
    def create(name: str, type: str = 'str', inner_type: str = None, inner_type_model_id: str = None, required: bool = False, default: str = None, choices: List[str] = None, description: str = None, type_properties: TypeProperties = None) -> 'DomainModelProperty':
        result = DomainModelProperty()
        result.name = name
        result.type = type
        result.inner_type = inner_type
        result.inner_type_model_id = inner_type_model_id
        result.required = required
        result.default = default
        result.choices = choices
        result.description = description
        result.type_properties = type_properties

        result.validate()
        return result


class AppDomainModel(Entity):
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_MODEL_TYPES)
    class_name = t.StringType(required=True)
    properties = t.ListType(t.ModelType(DomainModelProperty), default=[])
    dependencies = t.ListType(t.StringType())

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
        if property.type == 'value_object':
            self.dependencies.append(property.inner_type)
