from ...models import *


class DomainModelAttribute(Attribute):
    '''A domain model attribute.

    :param parent_model_id: The id of the parent domain model.
    :type parent_model_id: str
    :param name: The name of the attribute.
    :type name: str
    :param type: The type of the attribute.
    :type type: str
    :param inner_type: The inner type of the attribute.
    :type inner_type: str
    :param inner_type_model_id: The inner type model ID of the attribute.
    :type inner_type_model_id: str
    :param poly_type_model_ids: The poly type model IDs of the attribute.
    :type poly_type_model_ids: List[str]
    :param required: The required flag of the attribute.
    :type required: bool
    :param default: The default value of the attribute.
    :type default: str
    :param choices: The choices of the attribute.
    :type choices: List[str]
    :param description: The description of the attribute.
    :type description: str
    :param type_properties: The type properties of the attribute.
    :type type_properties: class: `domain.models.TypeProperties`
    '''

    parent_model_id = t.StringType(required=True)

    @staticmethod
    def create(name: str, parent_model_id: str,  type: str = 'str', inner_type: str = None, inner_type_model_id: str = None, poly_type_model_ids: List[str] = None, required: bool = None, default: str = None, choices: List[str] = None, description: str = None, type_properties: TypeProperties = None) -> 'DomainModelAttribute':
        result = DomainModelAttribute()
        result.name = name
        result.parent_model_id = parent_model_id
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
    

class DomainModelDependency(AppValueObject):
    
    model_id = t.StringType(required=True)
    class_name = t.StringType(required=True)
    dependency_type = t.StringType(required=True, choices=DOMAIN_MODEL_DEPENDENCY_TYPES, default=ATTRIBUTE_DEPENDENCY)
    module = t.StringType()

    @staticmethod
    def create(model_id: str, class_name: str, dependency_type: str = ATTRIBUTE_DEPENDENCY, module: str = None) -> 'DomainModelDependency':
        result = DomainModelDependency()
        result.model_id = model_id
        result.class_name = class_name
        result.dependency_type = dependency_type
        result.module = module

        result.validate()
        return result


class DomainModel(Class):

    type = t.StringType(required=True, choices=DOMAIN_MODEL_TYPES)
    base_type_model_id = t.StringType()
    attributes = t.ListType(t.ModelType(DomainModelAttribute), default=[])
    dependencies = t.ListType(t.ModelType(DomainModelDependency), default=[])
    methods = t.ListType(t.ModelType(DomainModelMethod), default=[])

    @staticmethod
    def create(name: str, type: str, class_name: str, description: str, id: str = None, base_type_model_id: str = None, attributes: List[DomainModelAttribute] = []) -> 'DomainModel':
        '''
        Creates a new Domain Model instance.

        :param name: The name of the domain model.
        :type name: str
        :param type: The type of the domain model.
        :type type: str
        :param class_name: The class name of the domain model.
        :type class_name: str
        :param description: The description of the domain model.
        :type description: str
        :param id: The id of the domain model.
        :type id: str
        :param base_type_model_id: The base type model id of the domain model.
        :type base_type_model_id: str
        :param attributes: The attributes of the domain model.
        :type attributes: List[DomainModelAttribute]
        :return: The new Domain Model instance.
        :rtype: class: `domain.modules.domain.models.DomainModel`
        '''
        
        result = DomainModel()
        result.name = name
        result.type = type
        result.class_name = class_name
        result.description = description
        result.base_type_model_id = base_type_model_id
        result.attributes = attributes

        # Convert python camel case to snake case if ID is not provided
        if id is None:
            import re
            result.id = name = re.sub(
            	r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        else:
            result.id = id

        result.validate()

        return result

    def has_attribute(self, attribute_name: str) -> bool:
        return any((p.name == attribute_name for p in self.attributes))

    def add_attribute(self, attribute: DomainModelAttribute) -> None:
        self.attributes.append(attribute)

    def get_attribute(self, attribute_name: str) -> DomainModelAttribute:
        return next((a for a in self.attributes if a.name == attribute_name), None)

    def remove_attribute(self, attribute: DomainModelAttribute) -> None:
        # Remove the attribute from the list.
        attributes: List[DomainModelAttribute] = [a for a in self.attributes if a.name != attribute.name]

        # Retrieve any potential dependencies of the attribute to be removed
        dependencies: List[DomainModelDependency] = []
        # If the attribute is a list or dict type, retrieve the dependencies as defined by the inner type model ID.
        if attribute.type in [LIST_TYPE, DICT_TYPE] and attribute.inner_type_model_id is not None:
            dependencies = [self.get_dependency(attribute.inner_type_model_id, ATTRIBUTE_DEPENDENCY)]

        # If the attribute is a model type, retrieve the dependencies as defined by the inner type.
        if attribute.type == MODEL_TYPE:
            dependencies = [self.get_dependency(attribute.inner_type, ATTRIBUTE_DEPENDENCY)]

        # If the attribute is a poly type, retrieve the dependencies as defined by the poly type model IDs.
        if attribute.type == POLY_TYPE:
            dependencies = [self.get_dependency(model_id, ATTRIBUTE_DEPENDENCY) for model_id in attribute.poly_type_model_ids]

        # Remove the dependencies only if no other attributes are dependent on them.
        for dependency in dependencies:
            if not any((a.has_dependency(dependency.model_id) for a in attributes)):
                self.remove_dependency(dependency)

        # Set the attributes to the new list.
        self.attributes = attributes

    def add_dependency(self, dependency: DomainModelDependency) -> None:
        if not any((d.model_id == dependency.model_id for d in self.dependencies)):
            self.dependencies.append(dependency)

    def get_dependency(self, model_id: str, dependency_type: str = ATTRIBUTE_DEPENDENCY) -> DomainModelDependency:
        return next((d for d in self.dependencies if d.model_id == model_id and d.dependency_type == dependency_type), None)

    def remove_dependency(self, dependency: DomainModelDependency) -> None:
        self.dependencies = [d for d in self.dependencies if d.model_id != dependency.model_id or d.dependency_type != dependency.dependency_type]

    def has_method(self, method: DomainModelMethod) -> bool:
        '''Checks to see if the model contains a method with the same name as the input.

        :param method: The input domain method to verify.
        :type method: class: `domain.models.DomainModelMethod`
        :return: True if the model contains a method with the same name as the input method.
        :rtype: bool
        '''
        # Return True if the model contains a method with the same name as the input method.
        return any((m.name == method.name for m in self.methods))
    
    def add_method(self, method: DomainModelMethod) -> None:
        '''Adds a new method to the domain model.

        :param method: The input domain method to add.
        :type method: class: `domain.models.DomainModelMethod`
        '''
        # Add the method to the methods list.
        self.methods.append(method)

    def get_method(self, method_name: str) -> DomainModelMethod:
        '''Returns the domain method with the input name.

        :param method_name: The name of the method to retrieve.
        :type method_name: str
        :return: The domain method with the input name.
        :rtype: class: `domain.models.DomainModelMethod`
        '''
        # Return the domain method with the input name.
        return next((m for m in self.methods if m.name == method_name), None)