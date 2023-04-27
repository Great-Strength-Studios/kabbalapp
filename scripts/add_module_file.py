import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--module', type=str, required=True)
parser.add_argument('-f', '--function', type=str, required=True)

args = parser.parse_args()

# Add module package directory.
module_package_directory = os.path.join('app', 'modules', args.module)
os.makedirs(module_package_directory, exist_ok=True)

# Add module file.
module_file_path = os.path.join(module_package_directory, '__init__.py')
with open(module_file_path, 'w') as f:
    f.write('')

# Add module function file.
module_function_file_path = os.path.join(module_package_directory, args.function + '.py')
with open(module_function_file_path, 'w') as f:
    f.writelines([
        'from ...core import *\n',
        'from ...domains import *\n',
        '\n',
        'def handle(context: MessageContext):\n'
        '\tpass',
    ])