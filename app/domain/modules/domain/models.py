from ...models import *


class DomainModelProperty(ModelProperty):

    type = t.StringType(required=True, choices=DOMAIN_PROPERTY_TYPES)
    inner_type_model_id = t.StringType()
    poly_type_model_ids = t.ListType(t.StringType())

    @staticmethod
    def create(name: str, type: str = 'str', inner_type: str = None, inner_type_model_id: str = None, poly_type_model_ids: List[str] = None, required: bool = None, default: str = None, choices: List[str] = None, description: str = None, type_properties: TypeProperties = None) -> 'DomainModelProperty':
        result = DomainModelProperty()
        result.name = name
        result.type = type
        result.inner_type = inner_type
        result.inner_type_model_id = inner_type_model_id
        result.poly_type_model_ids = poly_type_model_ids
        result.required = required
        result.default = default
        result.choices = choices
        result.description = description
        result.type_properties = type_properties

        result.validate()
        
        # Re-add type properties due to strange behavior with PolyType Model and validate
        result.type_properties = type_properties
        return result
    
    def has_dependency(self, model_id: str) -> bool:
        if self.type == MODEL_TYPE:
            return self.inner_type == model_id
        elif self.type == POLY_TYPE:
            return model_id in self.poly_type_model_ids
        elif self.type in [LIST_TYPE, DICT_TYPE]:
            return self.inner_type_model_id == model_id
        else:
            return False
    

class DomainModelDependency(ValueObject):
    model_id = t.StringType(required=True)
    class_name = t.StringType(required=True)
    dependency_type = t.StringType(required=True, choices=DOMAIN_MODEL_DEPENDENCY_TYPES)
    module = t.StringType()

    @staticmethod
    def create(model_id: str, class_name: str, dependency_type: str = 'property', module: str = None) -> 'DomainModelDependency':
        result = DomainModelDependency()
        result.model_id = model_id
        result.class_name = class_name
        result.dependency_type = dependency_type
        result.module = module

        result.validate()
        return result


class AppDomainModel(Entity):
    id = t.StringType(required=True)
    name = t.StringType(required=True)
    type = t.StringType(required=True, choices=DOMAIN_MODEL_TYPES)
    class_name = t.StringType(required=True)
    base_type_model_id = t.StringType()
    properties = t.ListType(t.ModelType(DomainModelProperty), default=[])
    dependencies = t.ListType(t.ModelType(DomainModelDependency), default=[])

    @staticmethod
    def create(name: str, type: str, class_name: str, id: str = None, base_type_model_id: str = None, properties: List[DomainModelProperty] = []) -> 'AppDomainModel':
        result = AppDomainModel()
        result.name = name
        result.type = type
        result.class_name = class_name
        result.base_type_model_id = base_type_model_id
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

    def get_property(self, property_name: str) -> DomainModelProperty:
        return next((p for p in self.properties if p.name == property_name), None)

    def remove_property(self, property: DomainModelProperty) -> None:
        # Remove the property from the list.
        properties: List[DomainModelProperty] = [p for p in self.properties if p.name != property.name]

        # Retrieve any potential dependencies of the property to be removed
        # If the property is a list or dict type, retrieve the dependencies as defined by the inner type model ID.
        if property.type in [LIST_TYPE, DICT_TYPE] and property.inner_type_model_id is not None:
            dependencies = [self.get_dependency(property.inner_type_model_id, 'property')]

        # If the property is a model type, retrieve the dependencies as defined by the inner type.
        if property.type == MODEL_TYPE:
            dependencies = [self.get_dependency(property.inner_type, 'property')]

        # If the property is a poly type, retrieve the dependencies as defined by the poly type model IDs.
        if property.type == POLY_TYPE:
            dependencies = [self.get_dependency(model_id, 'property') for model_id in property.poly_type_model_ids]

        # Remove the dependencies only if no other properties are dependent on them.
        for dependency in dependencies:
            if not any((p.has_dependency(dependency.model_id) for p in properties)):
                self.remove_dependency(dependency)

        # Set the properties to the new list.
        self.properties = properties

    def add_dependency(self, dependency: DomainModelDependency) -> None:
        if not any((d.model_id == dependency.model_id for d in self.dependencies)):
            self.dependencies.append(dependency)

    def get_dependency(self, model_id: str, dependency_type: str = 'property') -> DomainModelDependency:
        return next((d for d in self.dependencies if d.model_id == model_id and d.dependency_type == dependency_type), None)

    def remove_dependency(self, dependency: DomainModelDependency) -> None:
        self.dependencies = [d for d in self.dependencies if d.model_id != dependency.model_id or d.dependency_type != dependency.dependency_type]
