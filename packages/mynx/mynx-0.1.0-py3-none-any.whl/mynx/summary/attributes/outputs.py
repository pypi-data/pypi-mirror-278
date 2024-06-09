from flax.linen.module import _CallInfo
from flax.typing import MutableVariableDict
from colorama import Fore

from mynx.summary.attributes import Attribute

class Outputs(Attribute):
    attribute_name = "Outputs"
    line_lenght = 20
    
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        outputs = call.outputs
        shape = []
        for s in outputs.shape:
            shape.append([Fore.LIGHTGREEN_EX, str(s)])
            shape.append(["", ", "])
        shape.pop() 
        return [
            [Fore.CYAN, str(outputs.dtype)],
            [Fore.YELLOW, "["],
            *shape,
            [Fore.YELLOW, "]"]
        ]