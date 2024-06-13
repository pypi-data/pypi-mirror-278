from mynx.callbacks import Callback
from mynx.logs import Logs

class StepCounter(Callback):
    def __init__(self, epoch_steps:int):
        self.epoch_steps = epoch_steps

    def on_step_end(self, batch:int, logs:Logs):
        return f"{batch + 1}/{self.epoch_steps}"