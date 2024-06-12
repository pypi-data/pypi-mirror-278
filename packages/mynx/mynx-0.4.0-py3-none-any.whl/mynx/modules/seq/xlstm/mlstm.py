from typing import Tuple, Callable
from flax import linen as nn
from jax import numpy as jnp
from flax.typing import Array, Initializer
from typing import Optional
import jax

class MLSTMBlock(nn.Module):
    head_dim:int
    head_num:int
    ft_fn:Callable=jnp.exp
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array, hiden_state:Optional[Tuple[Array]]=None):
        skip = x
        x = nn.LayerNorm()(x)
        skip2 = nn.Dense(x.shape[-1] * 2, kernel_init=self.kernel_init)(x)
        skip2 = nn.silu(skip2)
        x = nn.Dense(x.shape[-1] * 2, kernel_init=self.kernel_init)(x)
        q_k = nn.Conv(x.shape[-1], 4)(x)
        q_k = nn.silu(q_k)
        skip3 = q_k
        x, hiden_state = MLSTMCell(head_dim=self.head_dim, head_num=self.head_num, ft_fn=self.ft_fn, kernel_init=self.kernel_init)(x, x, x, q_k, q_k, x, hiden_state)
        x = nn.GroupNorm(self.head_num)(x)
        x += skip3
        x *= skip2
        x = nn.Dense(skip.shape[-1], kernel_init=self.kernel_init)(x)
        return x + skip, hiden_state

class MLSTMCell(nn.Module):
    head_dim:int
    head_num:int
    ft_fn:Callable=jnp.exp
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, xi:Array, xf:Array, xo:Array, xq:Array, xk:Array, xv:Array, hiden_state:Optional[Tuple[Array]]=None):
        assert xi.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xf.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xo.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xq.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xk.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xv.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"

        zero_state = (
                    jnp.zeros((xi.shape[0], 1, self.head_num * self.head_dim, self.head_num * self.head_dim)),
                    jnp.ones((xi.shape[0], 1, self.head_num * self.head_dim))
                    )
        
        ct, nt = zero_state if hiden_state is None else hiden_state

        xi = xi.reshape(xi.shape[0], xi.shape[1], self.head_num, -1)
        xf = xf.reshape(xf.shape[0], xf.shape[1], self.head_num, -1)
        xo = xo.reshape(xo.shape[0], xo.shape[1], self.head_num, -1)
        xq = xq.reshape(xq.shape[0], xq.shape[1], self.head_num, -1)
        xk = xk.reshape(xk.shape[0], xk.shape[1], self.head_num, -1)
        xv = xv.reshape(xv.shape[0], xv.shape[1], self.head_num, -1)

        wi = self.param("wi", self.kernel_init, (xi.shape[-1], self.head_num, self.head_dim))
        wf = self.param("wf", self.kernel_init, (xf.shape[-1], self.head_num, self.head_dim))

        bi = self.param("bi", self.kernel_init, (1, self.head_dim))
        bf = self.param("bf", self.kernel_init, (1, self.head_dim))

        it = jnp.einsum("bshd,dho->bsho", xi, wi) + bi
        ft = jnp.einsum("bshd,dho->bsho", xf, wf) + bf
        it = it.reshape((it.shape[0], it.shape[1], -1))
        ft = ft.reshape((ft.shape[0], ft.shape[1], -1))
        ot = nn.Dense(self.head_num * self.head_dim, kernel_init=self.kernel_init)(xo)

        q = nn.Dense(self.head_num * self.head_dim, kernel_init=self.kernel_init)(xq)
        k = nn.Dense(self.head_num * self.head_dim, kernel_init=self.kernel_init)(xk)
        k = k / (self.head_num * self.head_dim)
        v = nn.Dense(self.head_num * self.head_dim, kernel_init=self.kernel_init)(xv)
        it = jnp.exp(it)
        ft = self.ft_fn(ft)
        ot = nn.sigmoid(ot)

        v *= it
        cn = v[..., None] * k[..., None, :]
        kn = it * k

        ct = jnp.concat([ct, cn], axis=1)
        nt = jnp.concat([nt, kn], axis=1)
        ft = jnp.concat([jnp.zeros((ft.shape[0], 1, ft.shape[2])), ft], axis=1)

        def step(cf1, cf2):
            f1, c1 = cf1
            f2, c2 = cf2
            return f1 * f2, f2 * c1 + c2
        
        _, ct = jax.lax.associative_scan(step, [ft[..., None], ct], axis=1)
        ct = ct[:, 1:]

        _, nt = jax.lax.associative_scan(step, [ft, nt], axis=1)
        nt = nt[:, 1:]

        ht = jnp.einsum("bsij,bsj->bsi", ct, q)
        ht /= jnp.maximum(jnp.abs(jnp.sum(nt * q, axis=-1)), 1)[..., None]
        ht *= ot
        return ht, (ct[:, -1:], nt[:, -1:])

