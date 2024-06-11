from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING

from hugr.serialization import ops

from guppylang.error import InternalGuppyError
from guppylang.tys.var import BoundVar, ExistentialVar

if TYPE_CHECKING:
    from guppylang.tys.ty import Type


@dataclass(frozen=True)
class Const(ABC):
    """Abstract base class for constants arguments in the type system.

    In principle, we can allow constants of any type representable in the type system.
    For now, we will only support basic consts like `int` or `bool`, but in the future
    we could have struct constants etc.
    """

    ty: "Type"

    def __post_init__(self) -> None:
        if self.ty.unsolved_vars:
            raise InternalGuppyError("Attempted to create constant with unsolved type")


@dataclass(frozen=True)
class ConstValue(Const):
    """A constant value in the type system.

    For example, in the type `array[int, 5]` the second argument is a `ConstArg`  that
    contains a `ConstValue(5)`.
    """

    # Hugr encoding of the value
    # TODO: We might need a Guppy representation of this...
    value: ops.Value


@dataclass(frozen=True)
class BoundConstVar(BoundVar, Const):
    """Bound variable referencing a `ConstParam`.

    For example, in the function type `forall n: int. array[float, n] -> array[int, n]`,
    we represent the int argument to `array` as a `ConstArg` containing a
    `BoundConstVar(idx=0)`.
    """


@dataclass(frozen=True)
class ExistentialConstVar(ExistentialVar, Const):
    """Existential constant variable.

    During type checking we try to solve all existential constant variables and
    substitute them with concrete constants.
    """

    @classmethod
    def fresh(cls, display_name: str, ty: "Type") -> "ExistentialConstVar":
        return ExistentialConstVar(ty, display_name, next(cls._fresh_id))
