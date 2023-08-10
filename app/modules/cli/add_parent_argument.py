from ...core import *
from ...domain import *

def handle(context: MessageContext):
	
    # Unpack request.
    request: AddCliParentArgument = context.data

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

    # Get cli parent command argument name or flags.
    name_or_flags = []
    if not request.positional:
        request.name = '--{}'.format(request.name.lower().replace('_', '-').replace(' ', '-'))
        if request.flags:
            request.flags = ['-{}'.format(flag.replace('_', '-')) for flag in request.flags]
    name_or_flags.append(request.name)
    if request.flags:
        name_or_flags.extend(request.flags)

    # Add parent command argument to cli interface.
    argument = service.add_parent_argument(name_or_flags=name_or_flags, **request.to_primitive('cli.add_parent_argument'))

    # If cli parent command argument already exists, raise exception.
    if isinstance(argument, tuple):
        raise AppError(context.errors.get(argument[0]).format_message(*argument[1:]))
    
    # Return cli parent command argument.
    return argument