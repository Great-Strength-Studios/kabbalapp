import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('subcommand')

parser.add_argument('--env', default='prod')
parser.add_argument('--debug', action='store_true')
parser.add_argument('--force', action='store_true')

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


args = parser.parse_args()
args = vars(args)
try:
    command = args.pop('command')
except KeyError:
    raise Exception('Invalid command input')
try:
    function = args.pop('subcommand')
except:
    raise Exception('Invalid subcommand input')