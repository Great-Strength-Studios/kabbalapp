from ...models import *

# Import dependencies
from .. import domain, domain as d


class TypePropertiesBlock(Model):

    type_properties = t.ModelType(TypeProperties, required=True)

    @staticmethod
    def create(type_properties: TypeProperties) -> 'TypePropertiesBlock':
        result = TypePropertiesBlock()
        result.type_properties = type_properties

        return result
    
    def print_lines(self):
        # Create empty list representing print lines
        print_lines = []


        # Add the type properties
        properties_list = []
        type_properties = self.type_properties.to_primitive()
        for key, value in type_properties.items():
            if not value:
                continue
            # Stringify the value if it is a string and key not in blacklist
            key_blacklist = ['coerce_key']
            if type(value) == str and key not in key_blacklist:
                value = f"'{value}'"
            properties_list.append(f'{key}={value}')

        # Join properties list with a comma and append to print lines
        print_lines.append(', '.join(properties_list))

        # Return list
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())


class DomainModelPropertyBlock(Model):

    property = t.ModelType(d.DomainModelProperty, required=True)
    dependencies = t.ListType(t.ModelType(d.DomainModelDependency))

    @staticmethod
    def create(property: d.DomainModelProperty, dependencies: List[d.DomainModelDependency] = None) -> 'DomainModelPropertyBlock':
        result = DomainModelPropertyBlock()
        result.property = property
        result.dependencies = dependencies

        return result
    
    def print_lines(self):
        # Create empty list representing print lines
        print_lines = []

        # Create the initial string with the tab indent.
        property_str = TAB

        # Add the name
        property_str += f'{self.property.name} = '

        # Add the type
        def map_type(type: str) -> str:
            if type == INT_TYPE:
                return 'Int'
            elif type == FLOAT_TYPE:
                return 'Float'
            elif type == BOOL_TYPE:
                return 'Boolean'
            elif type == STR_TYPE:
                return 'String'
            elif type == DATE_TYPE:
                return 'Date'
            elif type == DATETIME_TYPE:
                return 'DateTime'
            elif type == LIST_TYPE:
                return 'List'
            elif type == POLY_TYPE:
                return 'PolyModel'
            elif type == MODEL_TYPE:
                return 'Model'

        type_name = map_type(self.property.type)
        property_str += f't.{type_name}Type('

        if self.property.inner_type is not None:
            dependency = self.dependencies[0] if self.dependencies else None
            if self.property.type == MODEL_TYPE:
                property_str += f'{dependency.class_name}'
            elif self.property.inner_type == MODEL_TYPE:
                property_str += f't.ModelType({dependency.class_name})'
            else:
                property_str += f't.{map_type(self.property.inner_type)}Type'
        elif self.property.type == POLY_TYPE:
            poly_types = []
            for dependency in self.dependencies:
                poly_types.append(dependency.class_name)
            property_str += f'[{", ".join(poly_types)}]'

        # Create empty list for type arguments
        type_args = []

        # Add the required flag
        if self.property.required:
            type_args.append('required=True')
        
        # Add the default flag
        if self.property.default is not None:
            # Stringify the default if it the property type is a string
            if self.property.type == STR_TYPE:
                type_args.append(f"default='{self.property.default}'")
            else:
                type_args.append(f'default={self.property.default}')

        # Add the choices flag
        if self.property.choices:
            if self.property.type == STR_TYPE:
                choices = self.property.choices
            elif self.property.type == INT_TYPE:
                choices = [int(choice) for choice in self.property.choices]
            type_args.append(f'choices={str(choices)}')

        # If the property has type properties, add them
        if self.property.type_properties is not None:
            type_properties_block = TypePropertiesBlock.create(self.property.type_properties)
            type_args.extend(type_properties_block.print_lines())
        
        # Add the type args to the property string
        if len(type_args) > 0:
            if self.property.inner_type is not None:
                property_str += ', '
            property_str += ', '.join(type_args)
        
        # Close the type
        property_str += ')'

        # Add the property string to the print lines
        print_lines.append(property_str)

        # Return list
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())
        

class AppDomainModelBlock(Model):

    file_path = t.StringType(required=True)
    domain_models = t.ListType(t.ModelType(d.AppDomainModel), default=[])

    @staticmethod
    def create(project_path: str, domain_models: List[d.AppDomainModel]) -> 'AppDomainModelBlock':
        import os
        file_path = os.path.join(project_path, 'app', 'domain', 'models.py')

        result = AppDomainModelBlock()
        result.file_path = file_path
        result.domain_models = domain_models

        return result
    
    def add_domain_model(self, domain_model: d.AppDomainModel):
        self.domain_models.append(domain_model)

    def sort_dependencies(self):

        # Create empty list for sorted domain models
        sorted_domain_models = []

        # Create empty list for domain models that have not been sorted
        unsorted_domain_models = self.domain_models

        # Create empty list for domain models that have been sorted
        sorted_domain_models = []

        # Loop through unsorted domain models
        while len(unsorted_domain_models) > 0:

            # Loop through unsorted domain models
            for domain_model in unsorted_domain_models:

                # If the domain model has no dependencies, add it to the sorted domain models
                if not domain_model.dependencies or len(domain_model.dependencies) == 0:
                    sorted_domain_models.append(domain_model)
                    unsorted_domain_models.remove(domain_model)
                    continue

                # Loop through the domain model's dependencies
                for dependency in domain_model.dependencies:

                    # If the dependency is not in the unsorted domain models, skip it
                    if not any((d.id == dependency.model_id for d in unsorted_domain_models)):
                        continue

                    # Otherwise, break out of the loop
                    break

                # Otherwise, add the domain model to the sorted domain models
                else:
                    sorted_domain_models.append(domain_model)
                    unsorted_domain_models.remove(domain_model)
                    continue

        # Set the sorted domain models
        self.domain_models = sorted_domain_models

    def print_lines(self):
        # Create empty list representing print lines
        print_lines = []

        # Add import statements
        print_lines.append('from ..core.domain import *')
        print_lines.append('from .constants import *')

        # Reorder domain models such that value objects are first, then entities.
        self.domain_models.sort(key=lambda x: x.type, reverse=True)

        # Then sort the dependencies
        self.sort_dependencies()
        
        # Add value object classes
        # This will be done with a while loop to allow for skipping lines
        i = 0
        while i < len(self.domain_models):
             # Skip two lines first for formatting
            print_lines.append('')
            print_lines.append('')

            # Get the value object
            domain_model = self.domain_models[i]

            # Write out the class name and inheritance
            # If the domain model has a base model type, look for it on the dependency list and add it as a base type.
            # If type is entity, inherit from Entity. Else inherit from ValueObject
            # Otherwise just create a Model
            if domain_model.base_type_model_id:
                base_type = next((d for d in domain_model.dependencies if d.model_id == domain_model.base_type_model_id), None)
                print_lines.append(f'class {domain_model.class_name}({base_type.class_name}):')
            elif not domain_model.base_type_model_id and domain_model.type == 'value_object':
                print_lines.append(f'class {domain_model.class_name}(ValueObject):')
            elif not domain_model.base_type_model_id and domain_model.type == 'entity':
                print_lines.append(f'class {domain_model.class_name}(Entity):')
            else:
                print_lines.append(f'class {domain_model.class_name}(Model):')

            # If no properties exist, add a pass statement
            if len(domain_model.properties) == 0:
                print_lines.append(TAB + 'pass')
            else:
                # Otherwise add an extra line
                print_lines.append('')
            
            # Otherwise, add the properties
            for property in domain_model.properties:
                if property.type == 'poly':
                    dependencies = [d for d in domain_model.dependencies if d.model_id in property.poly_type_model_ids]
                else:
                    dependencies = [d for d in domain_model.dependencies if d.model_id == property.inner_type or d.model_id == property.inner_type_model_id]
                property_block = DomainModelPropertyBlock.create(property, dependencies)
                print_lines.extend(property_block.print_lines())
            
            # Increment the counter
            i += 1

        # Return list joined by newlines
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())