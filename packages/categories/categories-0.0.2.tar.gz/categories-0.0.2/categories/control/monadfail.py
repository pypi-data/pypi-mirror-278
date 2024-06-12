from __future__ import annotations

from typing import TypeVar

from categories.control.monad import Monad, MonadIO, MonadList
from categories.type import IO, hkt, typeclass

__all__ = (
    'MonadFail',
    'MonadFailIO',
    'MonadFailList',
)


a = TypeVar('a')

m = TypeVar('m')


class MonadFail(Monad[m], typeclass[m]):
    def fail(self, x : str, /) -> hkt[m, a]: ...


class MonadFailIO(MonadIO, MonadFail[IO]):
    async def fail(self, x : str, /) -> a:
        raise Exception(x)


class MonadFailList(MonadList, MonadFail[list]):
    def fail(self, _ : str, /) -> list[a]:
        return []
