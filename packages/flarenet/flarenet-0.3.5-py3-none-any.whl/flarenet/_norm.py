import flarejax as fj
import jax
from jaxtyping import Array, Float, jaxtyped

from ._activation import Standardize
from ._linear import Bias, Scale


class LayerNorm(fj.Module):
    __module_name = "flarenet.LayerNorm"

    norm: Standardize
    b: Bias
    s: Scale

    @fj.typecheck
    @classmethod
    def init(cls, dim: int, axis: int = -1):
        return cls(
            norm=Standardize(axis=axis),
            b=Bias.init(dim),
            s=Scale.init(dim),
        )

    @jaxtyped(typechecker=fj.typecheck)
    @jax.named_scope("flarenet.LayerNorm")
    def __call__(
        self,
        x: Float[Array, "*b {self.dim}"],
    ) -> Float[Array, "*b {self.dim}"]:
        return self.s(self.b(self.norm(x)))

    @fj.typecheck
    @property
    def dim(self) -> int:
        return self.b.dim
