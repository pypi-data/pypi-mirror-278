from flax.linen.module import _CallInfo
from flax.typing import MutableVariableDict
from flax.linen.summary import _get_call_flops
from colorama import Fore

from mynx.summary.attributes import Attribute

cache = {}
def get_call_flops(call):
    if not call.path in cache.keys():
        cache[call.path] = _get_call_flops(call, True, True)
    return cache[call.path]

class Flops(Attribute):
    attribute_name = "Flops"
    end_attribute_name = "Total Flops"
    line_lenght = 15
    
    def __init__(self):
        self.n_params = 0
        super().__init__()
    
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        flops, _ = get_call_flops(call)
        return [
            [Fore.MAGENTA, f"{flops:,}"]
        ]
    
    def end_attribute_compute(self, module, base_call, calls, variables):
        flops, _ = get_call_flops(base_call)
        return [
            [Fore.MAGENTA, f"{flops:,}"]
        ]
    
class VjpFlops(Attribute):
    attribute_name = "VjpFlops"
    end_attribute_name = "Total VjpFlops"
    line_lenght = 15
    
    def __init__(self):
        self.n_params = 0
        super().__init__()
    
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        _, vjp_flops = get_call_flops(call)
        return [
            [Fore.MAGENTA, f"{vjp_flops:,}"]
        ]
    
    def end_attribute_compute(self, module, base_call, calls, variables):
        _, vjp_flops = get_call_flops(base_call)
        return [
            [Fore.MAGENTA, f"{vjp_flops:,}"]
        ]