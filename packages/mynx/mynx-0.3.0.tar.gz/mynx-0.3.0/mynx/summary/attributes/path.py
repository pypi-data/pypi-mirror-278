from flax.linen.module import _CallInfo
from flax.typing import MutableVariableDict
from colorama import Fore

from mynx.summary.attributes import Attribute

class Path(Attribute):
    attribute_name = "Path"
    line_lenght = 20
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        path = []
        for p in call.path:
            path.append([Fore.LIGHTRED_EX, p])
            path.append([Fore.YELLOW, "/"])
        path.pop()
        return path