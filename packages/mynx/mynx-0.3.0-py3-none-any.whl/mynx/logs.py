from dataclasses import dataclass
from flax.training.train_state import TrainState

@dataclass
class Logs:
    state:TrainState=None
    batch:list=None
    loss:int=None
    y_pred:list=None