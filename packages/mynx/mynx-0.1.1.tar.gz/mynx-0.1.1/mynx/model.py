from flax import linen as nn
from flax.training.train_state import TrainState
from flax.training import common_utils
from flax import jax_utils
import flax.linen.module as module_lib
import optax
import jax.numpy as jnp
import jax
import math

from mynx import Logs, DataLoader
from mynx.summary import summary
from mynx.callbacks import Callback
from mynx.callbacks.metrics import EpochCounter, StepCounter, Loading, TimeTracing, Loss

class Model:
    def __init__(self, nn:nn.Module, loss, optimizer:optax.GradientTransformation, data_loader:DataLoader) -> None:
        self.nn = nn
        self.loss = loss
        self.optimizer = optimizer
        self.data_loader = data_loader

    def _step_fn(self, params, state, x, y_true, additional_data):
        y_pred = state.apply_fn({"params":params}, x)
        loss = self.loss(y_true, y_pred, additional_data)
        return loss, y_pred

    def _tran_step(self, state, x, y_true, additional_data):
        grad_fn = jax.value_and_grad(self._step_fn, has_aux=True, allow_int=True)
        (loss, y_pred), grads = grad_fn(state.params, state, x, y_true, additional_data)
        grads = jax.lax.pmean(grads, axis_name="devices")
        state = state.apply_gradients(grads=grads)
        return loss, y_pred, state

    def summary(self):
        summary(self.nn, jax.random.PRNGKey(0), self.data_loader.get_batch(0)[0])

    def fit(self, epochs:int = None, total_steps:int = None, callbecks:list[Callback] = [], default_callbecks=True):
        epoch_steps = len(self.data_loader)
        if total_steps:
            epochs = math.ceil(total_steps / epoch_steps)
        elif not epochs:
            raise ValueError("Missing argument epochs or total_steps")
        total_steps = epochs * epoch_steps
        
        self.callbecks:list[Callback] = []
        if default_callbecks:
            self.callbecks = [
                EpochCounter(epochs),
                StepCounter(epoch_steps),
                Loading(epoch_steps),
                TimeTracing(epoch_steps),
                Loss()
            ]
        self.callbecks += callbecks

        params = self.nn.init(jax.random.PRNGKey(0), self.data_loader.get_batch(0)[0])['params']
        self.state = TrainState.create(apply_fn=self.nn.apply, params=params, tx=self.optimizer)

        self._tran_step = jax.pmap(self._tran_step, axis_name="devices")

        logs = Logs(state=self.state)

        for callbeck in self.callbecks:
            callbeck.on_train_start(logs)

        total_start_step = logs.state.step
        start_epoch = total_start_step // epoch_steps
        start_step = total_start_step % epoch_steps
        print(start_step)
        self.data_loader.get_batch_idx.idx = start_step
        self.data_loader.start()

        self.device_state = jax_utils.replicate(logs.state)

        for epoch in range(start_epoch, epochs):

            msg = []
            for callbeck in self.callbecks:
                if callbeck_msg := callbeck.on_epoch_start(epoch, logs):
                    msg.append(callbeck_msg)
            if msg != []:
                msg = " - ".join(msg)
                print(msg)

            for idx in range(start_step, len(self.data_loader)):
                batch = next(self.data_loader)
                logs.batch = batch

                for callbeck in self.callbecks:
                    callbeck.on_step_start(idx, logs)

                shard_batch = jax.tree_util.tree_map(common_utils.shard, batch)
                loss, y_pred, self.device_state = self._tran_step(self.device_state, *shard_batch)
                loss = jnp.mean(loss)
                logs.loss = loss
                logs.y_pred = y_pred
                logs.state = jax_utils.unreplicate(self.device_state)

                last_msg_len = len(msg)
                msg = []
                for callbeck in self.callbecks:
                    if callbeck_msg := callbeck.on_step_end(idx, logs):
                        msg.append(callbeck_msg)
                if msg != []:
                    msg = " - ".join(msg)
                    if len(msg) < last_msg_len:
                        msg += " " * (last_msg_len - len(msg))
                    print("\r" + msg, end="")
            
            print()
            msg = []
            for callbeck in self.callbecks:
                if callbeck_msg := callbeck.on_epoch_end(epoch, logs):
                    msg.append(callbeck_msg)
            if msg != []:
                msg = " - ".join(msg)
                print(msg)
            
            start_step = 0

        for callbeck in self.callbecks:
            callbeck.on_train_end(logs)
        
        self.state = logs.state


