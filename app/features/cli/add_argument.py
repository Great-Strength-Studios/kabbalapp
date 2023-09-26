from ...core import *
from ...domain import *

def handle(context: MessageContext):
	
	# Unpack request.
	command_key = context.data.command_key
	subcommand_key = context.data.subcommand_key
	name = context.data.name
	help = context.data.help
	type = context.data.type
	flags = context.data.flags
	positional = context.data.positional
	default = context.data.default
	required = context.data.required
	choices = context.data.choices
	nargs = context.data.nargs
	action = context.data.action

	# Get app key from headers.
	app_key = context.headers.get('app_key', None)

	# If app key is not provided, raise exception.
	if not app_key:
		raise AppError(context.errors.APP_KEY_REQUIRED)
	
	# Get cli inteface repo.
	cli_interface_repo: CliInterfaceRepository = context.services.cli_interface_repo(app_key)

	# Retrieve cli interface
	interface = cli_interface_repo.get_inteface()

	# Raise interface type not found error if cli interface is not configured.
	if not interface:
		raise AppError(context.errors.INTERFACE_TYPE_NOT_FOUND.format_message('cli'))
	
	# Check to see if command exists.
	exists = interface.command_exists(command_key=command_key, subcommand_key=subcommand_key)

	# Raise command not found error if command does not exist.
	if not exists:
		raise AppError(context.errors.CLI_COMMAND_NOT_FOUND.format_message(command_key, subcommand_key))
	
	# Get cli command.
	command = interface.get_command(command_key=command_key, subcommand_key=subcommand_key)

	# Create new argument instance.
	argument = CliArgument.create(
		name=name,
		help=help,
		type=type,
		flags=flags,
		positional=positional,
		default=default,
		required=required,
		choices=choices,
		nargs=nargs,
		action=action)

	# Check to see if argument already exists.
	exists = command.argument_exists(argument.name_or_flags)

	# Raise argument already exists error if argument already exists.
	if exists:
		raise AppError(context.errors.CLI_ARGUMENT_ALREADY_EXISTS.format_message(str(argument.name_or_flags)))
	
	# Add argument to command.
	command.add_argument(argument)

	# Save cli interface.
	cli_interface_repo.save_interface(interface)

	# Return added argument.
	return argument