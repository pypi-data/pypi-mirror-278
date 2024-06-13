from __future__ import annotations

from typing import TypeVar

from categories.type import data, forall

__all__ = (
    'Maybe',
    'Nothing',
    'Just',
)


a = TypeVar('a')


@data(frozen=True)
class Nothing: ...


@data(frozen=True)
class Just(forall[a]):
    x : a


Maybe = Nothing | Just[a]