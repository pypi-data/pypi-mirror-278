from flax.linen.module import _CallInfo
from flax.typing import MutableVariableDict
from flax.linen.summary import _process_inputs
from colorama import Fore

from mynx.summary.attributes import Attribute

class Inputs(Attribute):
    attribute_name = "Inputs"
    line_lenght = 20
    
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        inputs = _process_inputs(call.args, call.kwargs)
        shape = []
        for s in inputs.shape:
            shape.append([Fore.LIGHTGREEN_EX, str(s)])
            shape.append(["", ", "])
        shape.pop() 
        return [
            [Fore.CYAN, str(inputs.dtype)],
            [Fore.YELLOW, "["],
            *shape,
            [Fore.YELLOW, "]"]
        ]