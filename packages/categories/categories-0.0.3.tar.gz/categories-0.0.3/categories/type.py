from __future__ import annotations

from builtins import frozenset as Set
from collections.abc import Callable as Expr
from collections.abc import Coroutine as Action
from collections.abc import Iterator as Stream
from dataclasses import dataclass as data
from types import MappingProxyType as Map
from typing import Annotated as hkt
from typing import Any as _
from typing import Generic as forall
from typing import NoReturn as Void
from typing import Protocol as typeclass
from typing import TypeVar

__all__ = (
    'Action',
    'Expr',
    'IO',
    'Lambda',
    'Map',
    'Set',
    'Stream',
    'Thunk',
    'Void',
    '_',
    'data',
    'forall',
    'hkt',
    'typeclass',
)


a = TypeVar('a')

b = TypeVar('b')


IO = Action[_, _, a]

Lambda = Expr[[a], b]

Thunk = Expr[[], a]
