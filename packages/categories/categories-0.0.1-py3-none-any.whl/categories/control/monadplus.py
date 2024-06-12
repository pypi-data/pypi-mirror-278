from __future__ import annotations

from typing import TypeVar

from categories.control.alternative import Alternative, AlternativeIO, AlternativeList
from categories.control.monad import Monad, MonadIO, MonadList
from categories.type import IO, hkt, typeclass

__all__ = (
    'MonadPlus',
    'MonadPlusIO',
    'MonadPlusList',
)


a = TypeVar('a')

m = TypeVar('m')


class MonadPlus(Alternative[m], Monad[m], typeclass[m]):
    def zero(self, /) -> hkt[m, a]:
        return self.empty()

    def plus(self, x : hkt[m, a], y : hkt[m, a], /) -> hkt[m, a]:
        return self.alt(x, y)


class MonadPlusIO(AlternativeIO, MonadIO, MonadPlus[IO]):
    async def zero(self, /) -> a:
        raise Exception('mzero')

    async def plus(self, m : IO[a], m_ : IO[a], /) -> a:
        try:
            return await m
        except BaseException:
            return await m_


class MonadPlusList(AlternativeList, MonadList, MonadPlus[list]): ...
