from __future__ import annotations

from typing import TypeVar

from categories.type import typeclass

__all__ = (
    'Show',
)


a = TypeVar('a')


class Show(typeclass[a]):
    def show(self, x : a, /) -> str: ...