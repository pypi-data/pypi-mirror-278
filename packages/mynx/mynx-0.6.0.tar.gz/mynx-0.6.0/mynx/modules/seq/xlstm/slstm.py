from typing import Tuple, Callable
from flax import linen as nn
from jax import numpy as jnp
from flax.typing import Array, Initializer
from typing import Optional

class SLSTMBlock(nn.Module):
    head_dim:int
    head_num:int
    ft_fn:Callable=jnp.exp
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, x:Array, hiden_state:Optional[Tuple[Array]]=None):
        skip = x
        x = nn.LayerNorm()(x)
        i_f = nn.Conv(x.shape[-1], 4, kernel_init=self.kernel_init)(x)
        i_f = nn.silu(i_f)
        x, hiden_state = SLSTMCell(head_dim=self.head_dim, head_num=self.head_num, ft_fn=self.ft_fn, kernel_init=self.kernel_init)(x, i_f, i_f, x, hiden_state)
        x = nn.GroupNorm(self.head_num)(x)
        x1 = nn.Dense(skip.shape[-1] * 4 // 3, kernel_init=self.kernel_init)(x)
        x2 = nn.Dense(skip.shape[-1] * 4 // 3, kernel_init=self.kernel_init)(x)
        x2 = nn.silu(x2)
        x = x1 * x2
        x = nn.Dense(skip.shape[-1], kernel_init=self.kernel_init)(x)
        return x + skip, hiden_state

class SLSTMCell(nn.Module):
    head_dim:int
    head_num:int
    ft_fn:Callable=jnp.exp
    kernel_init:Initializer=nn.initializers.lecun_normal()
    @nn.compact
    def __call__(self, xz:Array, xi:Array, xf:Array, xo:Array, hiden_state:Optional[Tuple[Array]]=None):
        assert xz.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xi.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xf.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        assert xo.shape[-1] % self.head_num == 0, "num of heads must by divisible by num of input dim"
        
        zero_state = (
                    jnp.zeros((*xz.shape[:-2], 1, self.head_num, self.head_dim)), 
                    jnp.zeros((*xz.shape[:-2], 1, self.head_num, self.head_dim)), 
                    jnp.zeros((*xz.shape[:-2], 1, self.head_num, self.head_dim))
                    )
        
        ct, ht, nt = zero_state if hiden_state is None else hiden_state

        xz = xz.reshape(*xz.shape[:-1], self.head_num, -1)
        xi = xi.reshape(*xi.shape[:-1], self.head_num, -1)
        xf = xf.reshape(*xf.shape[:-1], self.head_num, -1)
        xo = xo.reshape(*xo.shape[:-1], self.head_num, -1)

        wz = self.param("wz", self.kernel_init, (xz.shape[-1], self.head_num, self.head_dim))
        wi = self.param("wi", self.kernel_init, (xi.shape[-1], self.head_num, self.head_dim))
        wf = self.param("wf", self.kernel_init, (xf.shape[-1], self.head_num, self.head_dim))
        wo = self.param("wo", self.kernel_init, (xo.shape[-1], self.head_num, self.head_dim))

        bz = self.param("bz", self.kernel_init, (1, self.head_dim))
        bi = self.param("bi", self.kernel_init, (1, self.head_dim))
        bf = self.param("bf", self.kernel_init, (1, self.head_dim))
        bo = self.param("bo", self.kernel_init, (1, self.head_dim))

        rz = self.param("rz", self.kernel_init, (self.head_dim, self.head_num, self.head_dim))
        ri = self.param("ri", self.kernel_init, (self.head_dim, self.head_num, self.head_dim))
        rf = self.param("rf", self.kernel_init, (self.head_dim, self.head_num, self.head_dim))
        ro = self.param("ro", self.kernel_init, (self.head_dim, self.head_num, self.head_dim))

        szt = jnp.einsum("...ij,jik->...ik", xz, wz) + bz
        sit = jnp.einsum("...ij,jik->...ik", xi, wi) + bi
        sft = jnp.einsum("...ij,jik->...ik", xf, wf) + bf
        sot = jnp.einsum("...ij,jik->...ik", xo, wo) + bo

        out = []
        for zt, it, ft, ot in zip(*list(map(lambda x:jnp.split(x, x.shape[-3], axis=-3), (szt, sit, sft, sot)))):
            zt += jnp.einsum("...ij,jik->...ik", ht, rz)
            it += jnp.einsum("...ij,jik->...ik", ht, ri)
            ft += jnp.einsum("...ij,jik->...ik", ht, rf)
            ot += jnp.einsum("...ij,jik->...ik", ht, ro)

            zt = nn.tanh(zt)
            it = jnp.exp(it)
            ft = self.ft_fn(ft)
            ot = nn.sigmoid(ot)

            ct = ft * ct + it * zt
            nt = ft * nt + it

            ht = ct / nt
            ht = ot * ht
            out.append(ht)
        
        out = jnp.concat(out, axis=-3)
        out = out.reshape(*out.shape[:-2], -1)
        return out, (ct, ht, nt)