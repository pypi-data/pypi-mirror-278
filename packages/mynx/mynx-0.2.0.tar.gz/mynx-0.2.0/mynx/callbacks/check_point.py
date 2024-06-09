from pathlib import Path
import pickle

from mynx.callbacks import Callback
from mynx.logs import Logs

class CheckPoint(Callback):
    def __init__(self, path:Path):
        self.path = path
        super().__init__()

    def on_epoch_end(self, epoch: int, logs: Logs):
        with open(self.path, "wb") as f:
            pickle.dump(
                (
                    logs.state.step,
                    logs.state.params,
                    logs.state.opt_state
                ), 
                f
            )

    def on_train_start(self, logs: Logs):
        if not self.path.exists():
            return
        with open(self.path, "rb") as f:
            logs.state.step, logs.state.params, logs.state.opt_state = pickle.load(f)