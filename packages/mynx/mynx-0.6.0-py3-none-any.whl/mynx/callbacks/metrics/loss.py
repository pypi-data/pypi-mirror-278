from mynx.callbacks import Callback
from mynx.logs import Logs

class Loss(Callback):
    def on_step_end(self, batch: int, logs: Logs):
        return f"loss:{logs.loss:.4e}"