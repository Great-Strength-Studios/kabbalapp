from ...core import *
from ...domain import *

def handle(context: MessageContext):
	
	# Unpack request.
	request: AddCliSubcommand = context.data

	# Get app key from headers.
	app_key = context.headers.get('app_key', None)

	# If app key is not provided, raise exception.
	if not app_key:
		raise AppError(context.errors.APP_KEY_REQUIRED)
	
	# Get cli inteface service.
	service: cli.CliInterfaceService = context.services.cli_interface_service(app_key)

	# Format key if none is provided.
	if not request.key:
		request.key = request.name.lower().replace(' ', '_')

	# Add subcommand to cli interface.
	subcommand = service.add_subcommand(**request.to_primitive())

	# If cli subcommand already exists, raise exception.
	if isinstance(subcommand, tuple):
		raise AppError(context.errors.get(subcommand[0]).format_message(*subcommand[1:]))
	
	# Return cli subcommand.
	return subcommand