from __future__ import annotations

from typing import TypeVar

from categories.type import data, forall

__all__ = (
    'Dual',
    'getDual',
)


a = TypeVar('a')


@data(frozen=True)
class Dual(forall[a]):
    getDual : a


def getDual(x : Dual[a], /) -> a:
    match x:
        case Dual(getDual):
            return getDual