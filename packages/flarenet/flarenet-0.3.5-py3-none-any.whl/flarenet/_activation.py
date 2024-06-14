import flarejax as fj
import jax
from jaxtyping import Array, Float

import jax.nn as jnn

__all__ = [
    "ELU",
    "GLU",
    "CeLU",
    "HardSigmoid",
    "HardSiLU",
    "HardTanh",
    "LeakyReLU",
    "LogSigmoid",
    "LogSoftmax",
    "LogSumExp",
    "OneHot",
    "ReLU",
    "ReLU6",
    "SeLU",
    "Sigmoid",
    "SiLU",
    "Softmax",
    "SoftPlus",
    "SoftSign",
    "SparsePlus",
    "SquarePlus",
    "Standardize",
]


class CeLU(fj.Module):
    __module_name = "flarenet.CeLU"

    @fj.typecheck
    @jax.named_scope("flarenet.CeLU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.relu(x)


class ELU(fj.Module):
    __module_name = "flarenet.ELU"

    @fj.typecheck
    @jax.named_scope("flarenet.ELU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.elu(x)


class GLU(fj.Module):
    __module_name = "flarenet.GLU"

    axis: int = -1

    @fj.typecheck
    @jax.named_scope("flarenet.GLU")
    def __call__(self, x: Float[Array, "..."]) -> Float[Array, "..."]:
        return jnn.glu(x, self.axis)


class HardSigmoid(fj.Module):
    __module_name = "flarenet.HardSigmoid"

    @fj.typecheck
    @jax.named_scope("flarenet.HardSigmoid")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.hard_sigmoid(x)


class HardSiLU(fj.Module):
    __module_name = "flarenet.HardSiLU"

    @fj.typecheck
    @jax.named_scope("flarenet.HardSiLU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.hard_silu(x)


class HardTanh(fj.Module):
    __module_name = "flarenet.HardTanh"

    @fj.typecheck
    @jax.named_scope("flarenet.HardTanh")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.hard_tanh(x)


class LeakyReLU(fj.Module):
    __module_name = "flarenet.LeakyReLU"

    negative_slope: float = 1e-2

    @fj.typecheck
    @jax.named_scope("flarenet.LeakyReLU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.leaky_relu(x, self.negative_slope)


class LogSigmoid(fj.Module):
    __module_name = "flarenet.LogSigmoid"

    @fj.typecheck
    @jax.named_scope("flarenet.LogSigmoid")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.log_sigmoid(x)


class LogSoftmax(fj.Module):
    __module_name = "flarenet.LogSoftmax"

    @fj.typecheck
    @jax.named_scope("flarenet.LogSoftmax")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.log_softmax(x, axis=-1)


class LogSumExp(fj.Module):
    __module_name = "flarenet.LogSumExp"

    @fj.typecheck
    @jax.named_scope("flarenet.LogSumExp")
    def __call__(self, x: Float[Array, "..."]) -> Float[Array, "..."]:
        return jnn.logsumexp(x, axis=-1)


class Standardize(fj.Module):
    __module_name = "flarenet.Standardize"

    axis: int = -1

    @fj.typecheck
    @jax.named_scope("flarenet.Standardize")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.standardize(x, axis=self.axis)


class OneHot(fj.Module):
    __module_name = "flarenet.OneHot"

    num_classes: int
    axis: int = -1

    @fj.typecheck
    @jax.named_scope("flarenet.OneHot")
    def __call__(
        self,
        x: Float[Array, "*b"],
    ) -> Float[Array, "*b {self.dim}"]:
        return jnn.one_hot(x, self.num_classes, axis=self.axis)


class ReLU(fj.Module):
    __module_name = "flarenet.ReLU"

    @fj.typecheck
    @jax.named_scope("flarenet.ReLU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.relu(x)


class ReLU6(fj.Module):
    __module_name = "flarenet.ReLU6"

    @fj.typecheck
    @jax.named_scope("flarenet.ReLU6")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.relu6(x)


class SeLU(fj.Module):
    __module_name = "flarenet.SeLU"

    @fj.typecheck
    @jax.named_scope("flarenet.SeLU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.selu(x)


class Sigmoid(fj.Module):
    __module_name = "flarenet.Sigmoid"

    @fj.typecheck
    @jax.named_scope("flarenet.Sigmoid")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.sigmoid(x)


class SoftSign(fj.Module):
    __module_name = "flarenet.SoftSign"

    @fj.typecheck
    @jax.named_scope("flarenet.SoftSign")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.soft_sign(x)


class Softmax(fj.Module):
    __module_name = "flarenet.Softmax"

    axis: int = -1

    @fj.typecheck
    @jax.named_scope("flarenet.Softmax")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.softmax(x, axis=self.axis)


class SoftPlus(fj.Module):
    __module_name = "flarenet.SoftPlus"

    @fj.typecheck
    @jax.named_scope("flarenet.SoftPlus")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.softplus(x)


class SparsePlus(fj.Module):
    __module_name = "flarenet.SparsePlus"

    @fj.typecheck
    @jax.named_scope("flarenet.SparsePlus")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.sparse_plus(x)


class SiLU(fj.Module):
    __module_name = "flarenet.SiLU"

    @fj.typecheck
    @jax.named_scope("flarenet.SiLU")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.silu(x)


class SquarePlus(fj.Module):
    __module_name = "flarenet.SquarePlus"

    @fj.typecheck
    @jax.named_scope("flarenet.SquarePlus")
    def __call__(self, x: Float[Array, "*s"]) -> Float[Array, "*s"]:
        return jnn.squareplus(x)
