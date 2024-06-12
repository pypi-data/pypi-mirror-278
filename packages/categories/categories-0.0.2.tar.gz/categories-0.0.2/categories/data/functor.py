from __future__ import annotations

from typing import TypeVar

from categories.type import IO, Lambda, _, hkt, typeclass

__all__ = (
    'Functor',
    'FunctorIO',
    'FunctorLambda',
    'FunctorList',
)


a = TypeVar('a')

b = TypeVar('b')

f = TypeVar('f')

r = TypeVar('r')


class Functor(typeclass[f]):
    def map(self, f : Lambda[a, b], x : hkt[f, a], /) -> hkt[f, b]: ...


class FunctorIO(Functor[IO]):
    async def map(self, f : Lambda[a, b], m : IO[a], /) -> b:
        match await m:
            case x:
                return f(x)


class FunctorLambda(Functor[Lambda[r, _]]):
    def map(self, f : Lambda[a, b], g : Lambda[r, a], /) -> Lambda[r, b]:
        return lambda x, /: f(g(x))


class FunctorList(Functor[list]):
    def map(self, f : Lambda[a, b], xs : list[a], /) -> list[b]:
        return [f(x) for x in xs]
