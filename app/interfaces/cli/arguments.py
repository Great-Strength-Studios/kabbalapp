import sys, argparse
import yaml

from .config import *


with open('app/app.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
commands = AppCommandsConfiguration([i for i in app_config['interfaces'] if i['type'] == 'cli'][0])

# Create parser.
parser = argparse.ArgumentParser()

# Add command subparsers
command_subparsers = parser.add_subparsers(dest='command')
for command_name, command in commands.cli_commands.items():
    command_name = command_name.replace('_', '-')
    command_subparser = command_subparsers.add_parser(command_name, **command.to_primitive('add_parser'))
    subcommand_subparsers = command_subparser.add_subparsers(dest='subcommand')
    for subcommand_name, subcommand in command.cli_subcommands.items():
        subcommand_name = subcommand_name.replace('_', '-')
        subcommand_subparser = subcommand_subparsers.add_parser(subcommand_name, help=subcommand.help)
        for _, argument in subcommand.arguments.items():
            subcommand_subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))
        for _, argument in commands.parent_arguments.items():
            subcommand_subparser.add_argument(*argument.name_or_flags, **argument.to_primitive('add_argument'))

# Parse arguments.
args = parser.parse_args()
command = sys.argv[1].replace('-', '_')
subcommand = sys.argv[2].replace('-', '_')
args = vars(args)