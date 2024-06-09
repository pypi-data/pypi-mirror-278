from math import ceil

from mynx.callbacks import Callback
from mynx.logs import Logs

class Loading(Callback):
    def __init__(self, epoch_steps:int):
        self.epoch_steps = epoch_steps

    def on_step_end(self, batch:int, logs:Logs):
        batch = int((batch + 1) / self.epoch_steps * 20)
        loading = "=" * batch
        if (20 - batch) != 0:
            loading += ">"
        loading += " " * (20 - batch - 1)
        return f"[{loading}]"