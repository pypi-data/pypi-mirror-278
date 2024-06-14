import math

import flarejax as fj
import jax
import jax.numpy as jnp
import jax.random as jrandom
from jaxtyping import Array, Float, PRNGKeyArray, jaxtyped

__all__ = [
    "Linear",
]


class Linear(fj.Module):
    """
    Apply a learanable affine transformation to the input data. That takes the
    form of a matrix multiplication and an optional bias addition.

    The last input axis has dimensionality 'dim_in', the output shares all axes,
    except the last one with the input, which has dimensionality 'dim'.

    Attributes:
    ---
    w: jax.Array
        The learnable weights of the layer. This has shape (dim_in, dim).

    b: jax.Array | None
        The learnable bias of the layer. This has shape (dim,) or is None, if
        the layer does not have a bias.
    """

    __module_name = "flarenet.Linear"

    w: Array
    b: Array | None

    @fj.typecheck
    @classmethod
    def init(
        cls,
        key: PRNGKeyArray,
        dim_in: int,
        dim: int,
        use_bias: bool = True,
    ):
        """
        Initialize the layer with random weights and biases. The default
        initialization is based on the Glorot uniform initialization, which
        is the same as the PyTorch default.

        Parameters:
        ---
        key: PRNGKey
            The random key to use for initialization.

        dim_in: int
            The number of input features.

        dim: int
            The number of output features.

        use_bias: bool
            Whether to use a bias term in the layer.

        Returns:
        ---
        Linear
            The initialized layer.
        """
        scale = 1 / math.sqrt(dim_in)
        w_key, b_key = jrandom.split(key)

        w = jrandom.uniform(w_key, (dim_in, dim), minval=-1, maxval=1) * scale

        if use_bias:
            b = jrandom.uniform(b_key, (dim,), minval=-1, maxval=1) * scale
        else:
            b = None

        return cls(w=w, b=b)

    @jaxtyped(typechecker=fj.typecheck)
    @jax.named_scope("flarenet.Linear")
    def __call__(
        self,
        x: Float[Array, "*b dim_in"],
    ) -> Float[Array, "*b {self.dim}"]:
        y = jnp.dot(x, self.w)

        if self.has_bias:
            y += self.b

        return y

    @fj.typecheck
    @property
    def dim_in(self) -> int:
        return self.w.shape[0]

    @fj.typecheck
    @property
    def dim(self) -> int:
        return self.w.shape[1]

    @fj.typecheck
    @property
    def has_bias(self) -> bool:
        return self.b is not None


class Bias(fj.Module):
    __module_name = "flarenet.Bias"

    b: Array

    @fj.typecheck
    @classmethod
    def init(cls, dim: int):
        return cls(b=jnp.zeros((dim,)))

    @jaxtyped(typechecker=fj.typecheck)
    @jax.named_scope("flarenet.Bias")
    def __call__(
        self,
        x: Float[Array, "*b {self.dim}"],
    ) -> Float[Array, "*b {self.dim}"]:
        return x + self.b

    @fj.typecheck
    @property
    def dim(self) -> int:
        return self.b.shape[0]


class Scale(fj.Module):
    __module_name = "flarenet.Scale"

    s: Array

    @classmethod
    def init(cls, dim: int):
        return cls(s=jnp.ones((dim,)))

    @jax.named_scope("flarenet.Scale")
    def __call__(
        self, x: Float[Array, "*b {self.dim}"]
    ) -> Float[Array, "*b {self.dim}"]:
        return x * self.s

    @property
    def dim(self) -> int:
        return self.s.shape[0]
