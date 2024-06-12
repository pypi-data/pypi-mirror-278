from __future__ import annotations

from typing import TypeVar

from categories.control.monad import Monad
from categories.type import IO, hkt, typeclass

__all__ = (
    'MonadIO',
    'MonadIOIO',
)


a = TypeVar('a')

m = TypeVar('m')


class MonadIO(Monad[m], typeclass[m]):
    def liftIO(self, m : IO[a], /) -> hkt[m, a]: ...


class MonadIOIO(MonadIO[IO]):
    async def liftIO(self, m : IO[a], /) -> a:
        return await m
