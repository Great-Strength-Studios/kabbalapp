import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('subcommand')

parser.add_argument('--env', default='prod')
parser.add_argument('--debug', action='store_true')

parser.add_argument('-n', '--name')
parser.add_argument('-k', '--app-key')
parser.add_argument('-d', '--app-directory')

args = parser.parse_args()
args = vars(args)
try:
    command = args.pop('command')
except KeyError:
    raise Exception('Invalid command input')
try:
    function = [args.pop('subcommand')]
except:
    raise Exception('Invalid subcommand input')