from typing import TypeVar, Any

import flarejax as fj
import jax
import jax.numpy as jnp

T = TypeVar("T")


__all__ = [
    "Add",
    "Multiply",
    "Concat",
    "Identity",
    "Residual",
    "Index",
]


class Add(fj.Sequential):
    @fj.typecheck
    def __call__(self, x) -> Any:
        y = 0

        for module in self:
            assert callable(module), f"Module {module} is not callable."
            y = y + module(x)

        return y


class Multiply(fj.Sequential):
    @fj.typecheck
    def __call__(self, x) -> Any:
        y = 1

        for module in self:
            assert callable(module), f"Module {module} is not callable."
            y = y * module(x)

        return y


class Concat(fj.Sequential):

    @fj.typecheck
    def __call__(self, x) -> jax.Array:
        y = []

        for module in self:
            assert callable(module), f"Module {module} is not callable."
            y.append(module(x))

        return jnp.concatenate(y, axis=-1)


class Identity(fj.Module):

    @fj.typecheck
    def __call__(self, x: T) -> T:
        return x


class Residual(fj.Module):
    module: fj.Module

    @fj.typecheck
    def __call__(self, x) -> Any:
        assert callable(self.module), f"Module {self.module} is not callable."
        return x + self.module(x)


class Index(fj.Module):
    index: int | slice | tuple[int | slice, ...]

    @fj.typecheck
    def __call__(self, x) -> Any:
        return x[self.index]
