from typing import Union, Optional, Set, Tuple
from flax.typing import PRNGKey, RNGSequences
from flax.core.scope import CollectionFilter, DenyList
from flax.linen import module as module_lib
from flax.linen.summary import _get_path_variables, _process_inputs
import jax
from jax import tree_util
import math
from colorama import Fore

from mynx.summary.attributes import Path, Module, Inputs, Outputs, Params, Flops, VjpFlops

def summary(module:module_lib.Module, rngs: Union[PRNGKey, RNGSequences], *args, depth: Optional[int] = None, show_repeated: bool = False, mutable: CollectionFilter = DenyList('intermediates'), **kwargs):
    attributes = [
        Path(),
        Module(),
        Inputs(),
        Outputs(),
        Params(),
        Flops(),
        VjpFlops()
    ]
    with module_lib._tabulate_context():

        def _get_variables():
            return module.init(rngs, *args, **kwargs)
        
        variables = jax.eval_shape(_get_variables)
        calls = module_lib._context.call_info_stack[-1].calls
        calls.sort(key=lambda c:c.index)
        base_call = calls[0]
        calls = calls[1:]

    att_length = []
    headings = []
    for att in attributes:
        if att._att_name:
            att_length.append(att.line_lenght)
            headings.append(att.attribute_name)


    max_depth = 0
    to_display = []
    for c in calls:
        call_depth = len(c.path)
        if depth and call_depth > depth:
            continue
        if call_depth > max_depth:
            max_depth = call_depth
        counted_vars = _get_path_variables(c.path, variables)

        call_display = []
        for att in attributes:
            if att._att_fn:
                att_out = att.attribute_compute(c, counted_vars)
                if att._att_name:
                    call_display.append(att_out)
        to_display.append(call_display)
    
    total_info = StringList()
    idx = 0
    for att in attributes:
        if att._end_att_name:
            total_info[idx] = att.end_attribute_name
            total_info[idx] += ": "
            total_info[idx] += "".join(tree_util.tree_flatten(att.end_attribute_compute(module, base_call, calls, variables))[0])
            total_info[idx] += Fore.RESET
            idx += 1


    line = StringList()
    line[0] += "┏"
    for idx, al in enumerate(att_length):
        line[0] += "━"*al + "┳"
    line[0] = line[0][:-1] + "┓"
    print(line)

    line = StringList()
    for h, al  in zip(headings, att_length):
        idx = 0
        while h:
            line[idx] += "┃ "
            to_line = h[:al - 2]
            line[idx] += to_line
            h = h[al - 2:]
            line[idx] += " " * (al - len(to_line) - 1)
            idx += 1
    for idx in range(len(line)):
        line[idx] += "┃"
    
    print(line)

    line = StringList()
    line[0] += "┡"
    for idx, al in enumerate(att_length):
        line[0] += "━" * al + "╇"
    line[0] = line[0][:-1] + "┩"
    print(line)

    for line_idx, to_line in enumerate(to_display):
        line = StringList()

        heights = []
        for tls, al in zip(to_line, att_length):
            heights.append(math.ceil(sum([len(tl) for style, tl in tls]) / al))
        height = max(heights)

        for tls, al in zip(to_line, att_length):
            idx = 0
            last_idx = -1
            for style, tl in tls:
                while True:
                    if idx != last_idx:
                        line[idx] += "│ "
                        line_len = 0
                    last_idx = idx
                    line[idx] += style
                    to_line = tl[:al - 2 - line_len]
                    line_len += len(to_line)
                    line[idx] += to_line
                    line[idx] += Fore.RESET
                    tl = tl[al - 2:]
                    if tl == "":
                        break
                    idx += 1
            line[idx] += " " * (al - line_len - 1)
                    

            # for idx in range(height):
            #     line[idx] += "│ "
            #     line[idx] += style
            #     to_line = tl[:al - 2]
            #     line[idx] += to_line
            #     line[idx] += Fore.RESET
            #     tl = tl[al - 2:]
            #     line[idx] += " " * (al - len(to_line) - 1)

        if line_idx != len(to_display) - 1:
            line[height] += "├"
            for al in att_length:
                line[height] += "─" * al + "┼"
            line[height] = line[height][:-1] + "┤"
        else:
            line[height] += "└"
            for al in att_length:
                line[height] += "─" * al + "┴"
            line[height] = line[height][:-1] + "┘"

        for idx in range(len(line) - 1):
            line[idx] += "│"
        print(line)
    print()
    print(total_info)
    print()

class StringList:
    def __init__(self):
        self.data = dict()
        self.len = 0

    def __getitem__(self, idx):
        if idx not in self.data.keys():
            return ""
        return self.data[idx]
    
    def __setitem__(self, idx, value):
        if self.len <= idx:
            self.len = idx + 1
        self.data[idx] = value

    def __len__(self):
        return self.len
    
    def __str__(self):
        out = ""
        for idx in range(len(self)):
            out += self[idx] + "\n"
        out = out[:-1]
        return out
    
# if __name__ == "__main__":
#     s = StringList()

#     a = "asd"
#     a.
#     print(a)

#     for a in s.data:
#         print(a)