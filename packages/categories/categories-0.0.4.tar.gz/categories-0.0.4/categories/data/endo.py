from __future__ import annotations

from typing import TypeVar

from categories.type import Lambda, data, forall

__all__ = (
    'Endo',
    'appEndo',
)


a = TypeVar('a')


@data(frozen=True)
class Endo(forall[a]):
    appEndo : Lambda[a, a]


def appEndo(x : Endo[a], /) -> Lambda[a, a]:
    match x:
        case Endo(appEndo):
            return appEndo