from __future__ import annotations

from typing import TypeVar

from categories.control.monad import Monad
from categories.type import Lambda, hkt, typeclass

__all__ = (
    'MonadFix',
)


a = TypeVar('a')

m = TypeVar('m')


class MonadFix(Monad[m], typeclass[m]):
    def mfix(self, f : Lambda[a, hkt[m, a]], /) -> hkt[m, a]: ...