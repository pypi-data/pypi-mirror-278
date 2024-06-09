from time import time
from datetime import timedelta

from mynx.callbacks import Callback
from mynx.logs import Logs

class TimeTracing(Callback):
    def __init__(self, epoch_steps:int):
        self.start_time = 0
        self.epoch_steps = epoch_steps

    def get_highst_unit(self, t:timedelta):
        sec = t.total_seconds()
        if sec < 1 / 1000:
            return f"{round(sec * 1000 ** 2)} us"
        if sec < 1:
            return f"{round(sec * 1000)} ms"
        if sec < 60:
            return f"{round(sec)} s"
        if sec < 3600:
            return f"{round(sec // 60)} m"
        if sec < 86400:
            return f"{round(sec // 3600)} h"
        return f"{t.days} d"

    def on_epoch_start(self, epoch:int, logs:Logs):
        self.start_time = time()

    def on_step_end(self, batch:int, logs:Logs):
        time_to_step = timedelta(seconds=(time() - self.start_time) / (batch + 1))
        time_to_end = time_to_step * (self.epoch_steps - batch - 1)
        return f"ETA: {self.get_highst_unit(time_to_end)} - {self.get_highst_unit(time_to_step)}/step"