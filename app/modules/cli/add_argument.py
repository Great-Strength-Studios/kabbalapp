from ...core import *
from ...domain import *

def handle(context: MessageContext):
	
	# Unpack request.
	request: AddCliArgument = context.data

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

	# Format name or flags parameter
	request.name = request.name.lower().replace('_', '-').replace(' ', '-')
	if not request.positional:
		request.name = '--{}'.format(request.name)
		if request.flags:
			request.flags = ['-{}'.format(flag.replace('_', '-')) for flag in request.flags]
	name_or_flags = []
	name_or_flags.append(request.name)
	if request.flags:
		name_or_flags.extend(request.flags)

	# Format required parameter.
	if request.positional or request.required == False:
		request.required = None

	# Add argument to cli interface.
	argument = service.add_argument(name_or_flags=name_or_flags, **request.to_primitive('cli.add_argument'))

	# If cli argument already exists, raise exception.
	if isinstance(argument, tuple):
		raise AppError(context.errors.get(argument[0]).format_message(*argument[1:]))
	
	# Return cli argument.
	return argument