import sys, argparse

import yaml

from schematics import types as t, Model
from schematics.transforms import blacklist, whitelist
from schematics.types.serializable import serializable

class AppArgument(Model):
    name_or_flags = t.ListType(t.StringType(), required=True)
    help = t.StringType(required=True)
    type_str = t.StringType(default='str', choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType())
    action = t.StringType()

    @serializable
    def type(self):
        if self.type_str == 'str':
            return str
        elif self.type_str == 'int':
            return int
        elif self.type_str == 'float':
            return float
        else:
            raise Exception('Invalid type')
    
    class Options():
        serialize_when_none = False
        roles = {
            'add_argument': blacklist('type_str', 'name_or_flags')
        }

class AppSubcommand(Model):
    help = t.StringType(required=True)
    arguments = t.ListType(t.ModelType(AppArgument), default=[])

    class Options():
        serialize_when_none = False
        roles = {
            'add_subparser': blacklist('arguments')
        }

class AppCommand(Model):
    help = t.StringType(required=True)
    subcommands = t.DictType(t.ModelType(AppSubcommand), default=[])

    class Options():
        serialize_when_none = False
        roles = {
            'add_parser': blacklist('subcommands')
        }

class AppCommands(Model):
    parent_arguments = t.ListType(t.ModelType(AppArgument), default=[])
    commands = t.DictType(t.ModelType(AppCommand), default={})

with open('app/app.yml', 'r') as f:
    app_config = yaml.load(f.read())
commands = AppCommands(app_config['endpoints']['cmd'])

# Create parser.
parser = argparse.ArgumentParser()
for argument in commands.parent_arguments:
    parser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))

# Add command subparsers
command_subparsers = parser.add_subparsers(dest='command')
for command_name, command in commands.commands.items():
    command_subparser = command_subparsers.add_parser(command_name, command.to_primitive('add_parser'), parents=[parser])
    subcommand_subparsers = command_subparser.add_subparsers(dest='subcommand')
    for subcommand_name, subcommand in command.subcommands.items():
        subcommand_name = subcommand_name.replace('_', '-')
        subparser = subcommand_subparsers.add_parser(subcommand_name, help=subcommand.help)
        for argument in subcommand.arguments:
            subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))


parser.add_argument('command')
parser.add_argument('subcommand')



parser.add_argument('-n', '--name')
parser.add_argument('-k', '--key')
parser.add_argument('-d', '--app-directory')
parser.add_argument('-a', '--aliases', nargs='+')
parser.add_argument('-t', '--type')
parser.add_argument('-f', '--fields', nargs='+')
parser.add_argument('-m', '--metadata')

parser.add_argument('-ak', '--app-key')
parser.add_argument('-dk', '--domain-key')
parser.add_argument('-mk', '--model-key')
parser.add_argument('-cl', '--class-name')

command = sys.argv[1]
subcommand = sys.argv[2].replace('-', '_')
args = parser.parse_args()
args = vars(args)