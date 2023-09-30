from ..entities import *


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
        if self.property.type == 'int':
            type_name = 'Int'
        elif self.property.type == 'float':
            type_name = 'Float'
        elif self.property.type == 'str':
            type_name = 'String'
        property_str += f't.{type_name}Type('

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
            type_args.append(f'choices={str(self.property.choices)}')

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
        

class ValueObjectBlock(Model):

    file_path = t.StringType(required=True)
    value_objects = t.ListType(t.ModelType(ValueObject), default=[])

    @staticmethod
    def create(project_path: str, value_objects: list) -> 'ValueObjectBlock':
        import os
        file_path = os.path.join(project_path, 'app', 'domain', 'value_objects.py')

        result = ValueObjectBlock()
        result.file_path = file_path
        result.value_objects = value_objects

        return result
    
    def add_value_object(self, value_object: ValueObject):
        self.value_objects.append(value_object)

    def print_lines(self):
        # Create empty list representing print lines
        print_lines = []

        # Add import statements
        print_lines.append('from typing import List')
        print_lines.append('from schematics import types as t, Model')
        print_lines.append('from schematics.transforms import blacklist, whitelist')
        print_lines.append('from schematics.types.serializable import serializable')
        
        # Add value object classes
        # This will be done with a while loop to allow for skipping lines
        i = 0
        while i < len(self.value_objects):
             # Skip two lines first for formatting
            print_lines.append('')
            print_lines.append('')

            # Get the value object
            value_object = self.value_objects[i]

            # Write out the class name and inheritance
            print_lines.append(f'class {value_object.class_name}(Model):')

            # If no properties exist, add a pass statement
            if len(value_object.properties) == 0:
                print_lines.append('\tpass')
            
            # Otherwise, add the properties
            for property in value_object.properties:
                property_block = DomainModelPropertyBlock.create(property)
                print_lines.extend(property_block.print_lines())
            
            # Increment the counter
            i += 1

        # Return list joined by newlines
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())