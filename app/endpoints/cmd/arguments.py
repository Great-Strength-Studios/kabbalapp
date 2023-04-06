import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('subcommand')

parser.add_argument('--env', default='prod')
parser.add_argument('--debug', action='store_true')

args = parser.parse_args()
args = vars(args)
try:
    command = args.pop('command')
except KeyError:
    raise Exception('Invalid command input')
try:
    subcommand = args.pop('subcommand')
except:
    raise Exception('Invalid subcommand input')