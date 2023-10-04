from ...core import *
from ...domain import *

def handle(context: MessageContext):
	
    # Unpack request.
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
    cli_interface_repo: cli.CliInterfaceRepository = context.services.cli_interface_repo(app_key)

    # Get cli interface type.
    interface = cli_interface_repo.get_inteface()
    
    # Create new argument instance.
    argument = cli.CliArgument.create(
        name=name,
        help=help,
        type=type,
        flags=flags,
        positional=positional,
        default=default,
        required=required,
        choices=choices,
        nargs=nargs,
        action=action
    )

    # Check to see if argument already exists.
    exists = interface.parent_argument_exists(argument)

    # Raise parent argument exists error if parent argument already exists.
    if exists:
        raise AppError(context.errors.CLI_ARGUMENT_ALREADY_EXISTS.format_message(str(argument.name_or_flags)))

    # Add argument to interface.
    interface.add_parent_argument(argument)

    # Save interface.
    cli_interface_repo.save_interface(interface)

    # Return added argument.
    return argument