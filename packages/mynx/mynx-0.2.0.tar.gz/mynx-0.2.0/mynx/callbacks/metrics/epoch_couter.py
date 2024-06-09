from mynx.callbacks import Callback
from mynx.logs import Logs

class EpochCounter(Callback):
    def __init__(self, epochs:int):
        self.epochs = epochs

    def on_epoch_start(self, epoch:int, logs:Logs):
        return f"Epoch: {epoch + 1}/{self.epochs}"