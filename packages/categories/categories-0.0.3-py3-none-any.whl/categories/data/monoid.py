from __future__ import annotations

from functools import reduce
from typing import TypeVar

from categories.data.dual import Dual
from categories.data.endo import Endo
from categories.data.function import id
from categories.data.semigroup import Semigroup, SemigroupDual, SemigroupEndo
from categories.type import data, typeclass

__all__ = (
    'Monoid',
    'MonoidDual',
    'MonoidEndo',
)


a = TypeVar('a')


class Monoid(Semigroup[a], typeclass[a]):
    def empty(self, /) -> a:
        return self.concat([])

    def concat(self, xs : list[a], /) -> a:
        return reduce(self.append, xs, self.empty())


@data(frozen=True)
class MonoidDual(SemigroupDual[a], Monoid[Dual[a]]):
    inst : Monoid[a]

    def empty(self, /) -> Dual[a]:
        match self:
            case MonoidDual(inst):
                return Dual(inst.empty())


class MonoidEndo(SemigroupEndo[a], Monoid[Endo[a]]):
    def empty(self, /) -> Endo[a]:
        return Endo(id)
