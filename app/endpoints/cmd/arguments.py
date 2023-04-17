import argparse

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('subcommand')

parser.add_argument('--env', default='prod')
parser.add_argument('--debug', action='store_true')

parser.add_argument('-n', '--name')
parser.add_argument('-k', '--app-key')
parser.add_argument('-d', '--app-directory')

parser.add_argument('-dn', '--domain-name')
parser.add_argument('-dk', '--domain-key')

parser.add_argument('-mk', '--model-key')
parser.add_argument('-mn', '--model-name')
parser.add_argument('-mc', '--model-class')

parser.add_argument('-rk', '--role-key')
parser.add_argument('-rt', '--role-type')
parser.add_argument('-rf', '--role-fields', nargs='+')

parser.add_argument('-pn', '--property-name')
parser.add_argument('-pt', '--property-type')
parser.add_argument('-pr', '--property-required', action='store_true')
parser.add_argument('-psn', '--property-serialized-name')
parser.add_argument('-pdf', '--property-deserialize-from')
parser.add_argument('-pc', '--property-choices', nargs='+')
parser.add_argument('-pd', '--property-default')

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