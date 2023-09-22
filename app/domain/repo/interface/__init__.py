from ...value_objects import *
from ...entities import *
from ...modules import *

class AppInterfaceRepository():

    def get_interface(self, type: str) -> i.AppInterface:
        pass

    def save_interface(self, interface: i.AppInterface) -> None:
        pass