from __future__ import annotations

from functools import reduce
from itertools import repeat
from typing import TypeVar

from categories.data.dual import Dual
from categories.data.endo import Endo
from categories.data.function import o
from categories.type import data, typeclass

__all__ = (
    'Semigroup',
    'SemigroupDual',
    'SemigroupEndo',
)


a = TypeVar('a')


class Semigroup(typeclass[a]):
    def append(self, x : a, y : a, /) -> a:
        return self.concat([x, y])

    def concat(self, xs : list[a], /) -> a:
        return reduce(self.append, xs)

    def times(self, n : int, x : a, /) -> a:
        return reduce(self.append, repeat(x, n))


@data(frozen=True)
class SemigroupDual(Semigroup[Dual[a]]):
    inst : Semigroup[a]

    def append(self, x : Dual[a], y : Dual[a], /) -> Dual[a]:
        match (self, x, y):
            case SemigroupDual(inst), Dual(x_), Dual(y_):
                return Dual(inst.append(y_, x_))

    def times(self, n : int, x : Dual[a], /) -> Dual[a]:
        match (self, x):
            case SemigroupDual(inst), Dual(x_):
                return Dual(inst.times(n, x_))


class SemigroupEndo(Semigroup[Endo[a]]):
    def append(self, x : Endo[a], y : Endo[a], /) -> Endo[a]:
        match (x, y):
            case Endo(f), Endo(g):
                return Endo(o(f, g))

    def times(self, n : int, x : Endo[a], /) -> Endo[a]:
        match x:
            case Endo(f):
                return Endo(reduce(o, repeat(f, n)))
