from ...models import *
from .. import *


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
            # Stringify the value if it is a string
            if type(value) == str:
                value = f"'{value}'"
            properties_list.append(f'{key}={value}')

        # Join properties list with a comma and append to print lines
        print_lines.append(', '.join(properties_list))

        # Return list
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())


class DomainModelPropertyBlock(Model):

    property = t.ModelType(DomainModelProperty, required=True)

    @staticmethod
    def create(property: DomainModelProperty) -> 'DomainModelPropertyBlock':
        result = DomainModelPropertyBlock()
        result.property = property

        return result
    
    def print_lines(self):
        # Create empty list representing print lines
        print_lines = []

        # Create the initial string with the tab indent.
        property_str = '\t'

        # Add the name
        property_str += f'{self.property.name} = '

        # Add the type
        def map_type(type: str) -> str:
            if type == 'int':
                return 'Int'
            elif type == 'float':
                return 'Float'
            elif type == 'str':
                return 'String'
            elif type == 'list':
                return 'List'

        type_name = map_type(self.property.type)
        property_str += f't.{type_name}Type('

        if self.property.inner_type is not None:
            inner_type = map_type(self.property.inner_type)
            property_str += f't.{inner_type}Type(), '

        # Create empty list for type arguments
        type_args = []

        # Add the required flag
        if self.property.required:
            type_args.append('required=True')
        
        # Add the default flag
        if self.property.default is not None:
            type_args.append(f'default={self.property.default}')

        # Add the choices flag
        if self.property.choices:
            if self.property.type == 'str':
                choices = self.property.choices
            elif self.property.type == 'int':
                choices = [int(choice) for choice in self.property.choices]
            type_args.append(f'choices={str(choices)}')

        # If the property has type properties, add them
        if self.property.type_properties is not None:
            type_properties_block = TypePropertiesBlock.create(self.property.type_properties)
            type_args.extend(type_properties_block.print_lines())
        
        # Add the type args to the property string
        if len(type_args) > 0:
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
    domain_models = t.ListType(t.ModelType(AppDomainModel), default=[])

    @staticmethod
    def create(project_path: str, domain_models: List[AppDomainModel]) -> 'AppDomainModelBlock':
        import os
        file_path = os.path.join(project_path, 'app', 'domain', 'models.py')

        result = AppDomainModelBlock()
        result.file_path = file_path
        result.domain_models = domain_models

        return result
    
    def add_domain_model(self, domain_model: AppDomainModel):
        self.domain_models.append(domain_model)

    def print_lines(self):
        # Create empty list representing print lines
        print_lines = []

        # Add import statements
        print_lines.append('from ..core.domain import *')
        print_lines.append('from .constants import *')

        # Reorder domain models such that value objects are first, then entities.
        self.domain_models.sort(key=lambda x: x.type, reverse=True)
        
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
            # If type is entity, inherit from Entity. Else inherit from ValueObject
            # Otherwise just create a Model
            if domain_model.type == 'value_object':
                print_lines.append(f'class {domain_model.class_name}(ValueObject):')
            elif domain_model.type == 'entity':
                print_lines.append(f'class {domain_model.class_name}(Entity):')
            else:
                print_lines.append(f'class {domain_model.class_name}(Model):')

            # If no properties exist, add a pass statement
            if len(domain_model.properties) == 0:
                print_lines.append('\tpass')
            
            # Otherwise, add the properties
            for property in domain_model.properties:
                property_block = DomainModelPropertyBlock.create(property)
                print_lines.extend(property_block.print_lines())
            
            # Increment the counter
            i += 1

        # Return list joined by newlines
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())