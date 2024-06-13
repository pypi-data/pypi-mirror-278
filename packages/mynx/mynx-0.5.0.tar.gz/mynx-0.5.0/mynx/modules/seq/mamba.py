from flax import linen as nn
from jax import numpy as jnp
from flax.typing import Array, Initializer
from typing import Optional
import jax

class Mamba(nn.Module):
    dim:int
    state_dim:int
    kernel_size:int=3
    is_training:bool=True
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array, hiden_state:Optional[Array]=None):
        dim = x.shape[-1]

        x1 = nn.Dense(self.dim, kernel_init=self.kernel_init)(x)
        x2 = nn.Dense(self.dim, kernel_init=self.kernel_init)(x)

        x1 = nn.Conv(self.dim, 3, kernel_init=self.kernel_init)(x1)
        x1 = nn.silu(x1)
        x1, hiden_state = SSM(state_dim=self.state_dim, is_training=self.is_training, kernel_init=self.kernel_init)(x1, hiden_state)

        x2 = nn.silu(x2)

        x = x1 * x2
        x = nn.Dense(dim, kernel_init=self.kernel_init)(x)
        return x, hiden_state

class SSM(nn.Module):
    state_dim:int
    is_training:bool=True
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array, hiden_state:Optional[Array]=None):
        dim = x.shape[-1]

        delta = nn.Dense(self.state_dim, use_bias=False)(x)
        a = self.param("a", self.kernel_init, (1, self.state_dim))
        b = self.param("b", self.kernel_init, (1, self.state_dim))
        delta *= a + 1j * b
        weights = jnp.exp(delta)

        x = nn.Dense(self.state_dim, use_bias=False, param_dtype=jnp.complex64, kernel_init=self.kernel_init)(x)

        def step(wx1, wx2):
            w1, x1 = wx1
            w2, x2 = wx2
            return w1 * w2, w2 * x1 + x2
        
        if self.is_training:
            _, out = jax.lax.associative_scan(step, [weights, x], axis=-2)
        else:
            if hiden_state is None:
                out = x
            else:
                out = weights * hiden_state + x
            hiden_state = out

        out = nn.Dense(dim, use_bias=False, param_dtype=jnp.complex64, kernel_init=self.kernel_init)(out)
        return jnp.real(out), hiden_state