from .value_objects import *
from .entities import *
from .modules import *

def create_cli_interface() -> cli.CliAppInterface:
    interface = cli.CliAppInterface()
    interface.type = 'cli'

    return interface