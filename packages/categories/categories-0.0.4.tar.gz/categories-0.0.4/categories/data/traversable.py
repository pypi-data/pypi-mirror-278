from __future__ import annotations

from typing import TypeVar

from categories.control.applicative import Applicative
from categories.control.monad import Monad
from categories.data.foldable import Foldable
from categories.data.functor import Functor
from categories.type import Lambda, hkt, typeclass

__all__ = (
    'Traversable',
)


a = TypeVar('a')

b = TypeVar('b')

f = TypeVar('f')

m = TypeVar('m')

t = TypeVar('t')


class Traversable(Functor[t], Foldable[t], typeclass[t]):
    def traverse(self, inst : Applicative[f],
                 f : Lambda[a, hkt[f, b]], xs : hkt[t, a], /) -> hkt[f, hkt[t, b]]:
        return self.sequenceA(inst, self.map(f, xs))

    def sequenceA(self, inst : Applicative[f],
                  xs : hkt[t, hkt[f, a]], /) -> hkt[f, hkt[t, a]]:
        return self.traverse(inst, lambda x, /: x, xs)

    def mapM(self, inst : Monad[m],
             f : Lambda[a, hkt[m, b]], xs : hkt[t, a], /) -> hkt[m, hkt[t, b]]:
        return self.traverse(inst, f, xs)

    def sequence(self, inst : Monad[m],
                 xs : hkt[t, hkt[m, a]], /) -> hkt[m, hkt[t, a]]:
        return self.sequenceA(inst, xs)
