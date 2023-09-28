from ..entities import *

class ModelPropertyBlock(Model):

    property = t.ModelType(ModelProperty, required=True)

    @staticmethod
    def create(property: ModelProperty) -> 'ModelPropertyBlock':
        result = ModelPropertyBlock()
        result.property = property

        return result


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
            
            # Increment the counter
            i += 1

        # Return list joined by newlines
        return print_lines
    
    def print(self):
        return '\n'.join(self.print_lines())