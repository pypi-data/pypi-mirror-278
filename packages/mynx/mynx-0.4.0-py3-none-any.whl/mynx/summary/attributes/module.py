from flax.linen.module import _CallInfo
from flax.typing import MutableVariableDict
from colorama import Fore

from mynx.summary.attributes import Attribute

class Module(Attribute):
    attribute_name = "Module"
    line_lenght = 20
    
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        return [
            [Fore.RED, call.module.name]
        ]