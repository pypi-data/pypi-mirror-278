from pathlib import Path
import pickle
from flax.training.train_state import TrainState

from mynx.callbacks import Callback
from mynx.logs import Logs

class CheckPoint(Callback):
    def __init__(self, path:Path):
        self.path = path
        super().__init__()

    def on_epoch_end(self, epoch: int, logs: Logs):
        if not self.path.exists():
            self.path.parent.mkdir()
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
            step, params, opt_state = pickle.load(f)
        logs.state = TrainState(step=step, apply_fn=logs.state.apply_fn, params=params, tx=logs.state.tx, opt_state=opt_state)