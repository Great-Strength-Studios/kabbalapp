from ...models import *

# Module dependencies
from .. import interface, interface as i


class CliArgument(AppValueObject):
    name_or_flags = t.ListType(t.StringType, required=True)
    help = t.StringType(required=True)
    type = t.StringType(choices=['str', 'int', 'float'])
    default = t.StringType()
    required = t.BooleanType()
    nargs = t.StringType()
    choices = t.ListType(t.StringType)
    action = t.StringType()

    @staticmethod
    def create(name: str, help: str, type: str = None, flags: List[str] = [], positional: bool = False, default: str = None, required: bool = False, nargs: str = None, choices: List[str] = None, action: str = None):
        argument = CliArgument()

        # Format name or flags parameter
        name = name.lower().replace('_', '-').replace(' ', '-')
        if not positional:
            name = '--{}'.format(name)
            if flags:
                flags = ['-{}'.format(flag.replace('_', '-')) for flag in flags]
        name_or_flags = []
        name_or_flags.append(name)
        if flags:
            name_or_flags.extend(flags)

        # Format required parameter.
        if positional or required == False:
            required = None

        # Set argument properties
        argument.name_or_flags = name_or_flags
        argument.help = help
        argument.type = type
        argument.default = default
        argument.required = required
        argument.nargs = nargs
        argument.choices = choices
        argument.action = action

        # Return argument
        return argument


class CliCommand(Entity):
    command_key = t.StringType(required=True)
    subcommand_key = t.StringType()
    help = t.StringType(required=True)
    arguments = t.ListType(t.ModelType(CliArgument), default=[])

    @staticmethod
    def create(command_key: str, name: str, help: str, subcommand_key: str = None, arguments: List[CliArgument] = []):
        command = CliCommand()
        command.command_key = command_key
        command.name = name
        command.help = help
        command.subcommand_key = subcommand_key
        command.arguments = arguments

        command.id = command_key
        if subcommand_key:
            command.id = '{}.{}'.format(command_key, subcommand_key)

        return command
    
    def argument_exists(self, flags: List[str]):
        # Loop through the flags and check if any of them match the flags of an existing argument
        for flag in flags:
            if any([argument for argument in self.arguments if flag in argument.name_or_flags]):
                return True
        # Return False if no argument was found
        return False
    
    def add_argument(self, argument: CliArgument) -> None:
        self.arguments.append(argument)


class CliInterfaceType(i.AppInterfaceType):
    mappers = t.DictType(t.StringType)
    commands = t.ListType(t.ModelType(CliCommand), default=[])
    parent_arguments = t.ListType(t.ModelType(CliArgument), default=[])

    @staticmethod
    def create(name: str, type: str):
        interface = CliInterfaceType()
        interface.name = name
        interface.type = type

        return interface
    
    def command_exists(self, command_key: str, subcommand_key: str = None) -> bool:
        return any([command for command in self.commands if command.command_key == command_key and command.subcommand_key == subcommand_key])
    
    def add_command(self, command: CliCommand) -> None:
        self.commands.append(command)

    def get_command(self, command_key: str, subcommand_key: str = None) -> CliCommand:
        return next(
            (
                command for command in self.commands 
                if command.command_key == command_key 
                and command.subcommand_key == subcommand_key
            ), 
            None
        )

    def parent_argument_exists(self, argument: CliArgument) -> bool:
        # Loop through the flags and check if any of them match the flags of an existing parent argument
        for flag in argument.name_or_flags:
            if any([argument for argument in self.parent_arguments if flag in argument.name_or_flags]):
                return True
        # Return False if no argument was found
        return False
    
    def add_parent_argument(self, argument: CliArgument) -> None:
        self.parent_arguments.append(argument)