from __future__ import annotations

from asyncio import gather, run
from typing import TypeVar

from categories.type import IO, Lambda

__all__ = (
    'run',
    'returnIO',
    'bindIO',
    'thenIO',
    'failIO',
    'mplusIO',
    'sequenceIO',
)


a = TypeVar('a')

b = TypeVar('b')


async def returnIO(x : a, /) -> a:
    return x


async def bindIO(m : IO[a], k : Lambda[a, IO[b]], /) -> b:
    match await m:
        case x:
            return await k(x)


async def thenIO(m : IO[a], k : IO[b], /) -> b:
    match await m:
        case _:
            return await k


async def failIO(x : str, /) -> a:
    raise Exception(x)


async def mplusIO(m : IO[a], m_ : IO[a], /) -> a:
    try:
        return await m
    except BaseException:
        return await m_


async def sequenceIO(xs : list[IO[a]], /) -> list[a]:
    return await gather(*xs)