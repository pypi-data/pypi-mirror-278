from typing import Any, Callable
from flax import linen as nn
from jax import numpy as jnp
from flax.typing import Array, Initializer
from itertools import starmap
import jax

class MOE(nn.Module):
    expert_init:Callable
    expert_num:int
    expert_topk:int
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array) -> Array:
        experts = [self.expert_init() for _ in range(self.expert_num)]

        gating = nn.Dense(self.expert_num, use_bias=False, kernel_init=self.kernel_init)(x)
        _, indices = jax.lax.top_k(gating, self.expert_topk)
        
        mask = nn.one_hot(indices, self.expert_num)
        mask = jnp.sum(mask, axis=-2)
        gating -= 1 / mask - 1
        gating = nn.softmax(gating)

        mask = jnp.split(mask, self.expert_num, axis=-1)
        gating = jnp.split(gating, self.expert_num, axis=-1)

        out = list(starmap(lambda mask, gate, expert:expert(x * mask) * gate, zip(mask, gating, experts)))
        out = sum(out)
        
        return out
    
class MultiHeadMOE(nn.Module):
    expert_init:Callable
    expert_num:int
    expert_topk:int
    head_num:int
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array):
        assert x.shape[-1] % self.head_num == 0, "dims must be devisible by num of heads"

        dim = x.shape[-1]

        x = nn.Dense(dim, use_bias=False, kernel_init=self.kernel_init)(x)
        x = x.reshape((*x.shape[:-1], self.head_num, -1))
        x = MOE(expert_init=self.expert_init, expert_num=self.expert_num, expert_topk=self.expert_topk, kernel_init=self.kernel_init)(x)
        x = x.reshape((*x.shape[:-2], -1))
        x = nn.Dense(dim, use_bias=False, kernel_init=self.kernel_init)(x)

        return x
    
class SoftMOE(nn.Module):
    expert_init:Callable
    expert_num:int
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array):
        experts = [self.expert_init() for _ in range(self.expert_num)]

        gating = nn.Dense(self.expert_num, use_bias=False, kernel_init=self.kernel_init)(x)
        dis = nn.softmax(gating, axis=-2)
        com = nn.softmax(gating, axis=-1)

        x = jnp.einsum("...sd,...se->...ed", x, dis)

        x = jnp.split(x, self.expert_num, axis=-2)
        x = list(starmap(lambda expert, x:expert(x), zip(experts, x)))
        x = jnp.concat(x, axis=-2)

        x = jnp.einsum("...ed,...se->...sd", x, com)

        return x
