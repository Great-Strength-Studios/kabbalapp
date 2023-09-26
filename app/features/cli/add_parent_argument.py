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
    cli_interface_repo: CliInterfaceRepository = context.services.cli_interface_repo(app_key)

    # Get cli parent command argument name or flags.
    name_or_flags = []
    if not positional:
        name = '--{}'.format(name.lower().replace('_', '-').replace(' ', '-'))
        if flags:
            flags = ['-{}'.format(flag.replace('_', '-')) for flag in flags]
    name_or_flags.append(name)
    if flags:
        name_or_flags.extend(flags)

    # Get cli interface type.
    interface = cli_interface_repo.get_inteface()

    # Check to see if argument already exists.
    exists = interface.parent_argument_exists(name_or_flags)

    # Raise parent argument exists error if parent argument already exists.
    if exists:
        raise AppError(context.errors.CLI_ARGUMENT_ALREADY_EXISTS.format_message(str(name_or_flags)))
    
    # Create new argument instance.
    argument = CliArgument.create(
        name_or_flags=name_or_flags,
        help=help,
        type=type,
        default=default,
        required=required,
        choices=choices,
        nargs=nargs,
        action=action
    )

    # Add argument to interface.
    interface.add_parent_argument(argument)

    # Save interface.
    cli_interface_repo.save_interface(interface)

    # Return added argument.
    return argument