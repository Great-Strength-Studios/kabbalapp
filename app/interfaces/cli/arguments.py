import sys, argparse
import yaml

from .config import *


with open('app/app.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

# Get app interface types
interfaces = app_config.get('interfaces', None)
types = app_config.get('types', None)

# Print a message if no interface types are configured
if interfaces is None:
    print('No interfaces configured.')
    sys.exit(0)
# Get cli interface
cli_interface = types.get('cli', None)
# Print a message if not cli interface is configured
if cli_interface is None:
    print('No cli interface configured.')
    sys.exit(0)

cli_interface = CliInterfaceConfiguration(cli_interface)

# Create parser.
parser = argparse.ArgumentParser()

# Add command subparsers
command_subparsers = parser.add_subparsers(dest='command')
for command_name, command in cli_interface.commands.items():
    command_name = command_name.replace('_', '-')
    command_subparser = command_subparsers.add_parser(command_name, **command.to_primitive('add_parser'))
    subcommand_subparsers = command_subparser.add_subparsers(dest='subcommand')
    for subcommand_name, subcommand in command.subcommands.items():
        subcommand_name = subcommand_name.replace('_', '-')
        subcommand_subparser = subcommand_subparsers.add_parser(subcommand_name, help=subcommand.help)
        for argument in subcommand.arguments:
            subcommand_subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))
        for _, argument in cli_interface.parent_arguments.items():
            subcommand_subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))

# Parse arguments.
args = parser.parse_args()
command = sys.argv[1].replace('-', '_')
subcommand = sys.argv[2].replace('-', '_')
args = vars(args)