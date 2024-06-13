from flax.linen.module import _CallInfo
from flax.typing import MutableVariableDict
from jax import tree_util
from functools import reduce
from colorama import Fore

from mynx.summary.attributes import Attribute

class Params(Attribute):
    attribute_name = "Params"
    end_attribute_name = "Total Parameters"
    line_lenght = 15
    
    def __init__(self):
        self.n_params = 0
        super().__init__()
    
    def attribute_compute(self, call:_CallInfo, vars:MutableVariableDict):
        n_params = sum([reduce((lambda x, y: x * y), w.shape) for w in tree_util.tree_flatten(vars)[0]])
        if len(call.path) == 1:
            self.n_params += n_params
        return [
            [Fore.GREEN, f"{n_params:,}"]
        ]
    
    def end_attribute_compute(self, case_coll, module, calls, variables):
        return [
            [Fore.GREEN, f"{self.n_params:,}"]
        ]