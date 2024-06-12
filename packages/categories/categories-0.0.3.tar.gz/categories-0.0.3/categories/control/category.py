from __future__ import annotations

from typing import TypeVar

from categories.type import Lambda, hkt, typeclass

__all__ = (
    'Category',
    'CategoryLambda',
    'arrow',
)


a = TypeVar('a')

b = TypeVar('b')

c = TypeVar('c')

cat = TypeVar('cat')


class Category(typeclass[cat]):
    def id(self, /) -> hkt[cat, a, a]: ...

    def o(self, f : hkt[cat, b, c], g : hkt[cat, a, b], /) -> hkt[cat, a, c]: ...


class CategoryLambda(Category[Lambda]):
    def id(self, /) -> Lambda[a, a]:
        return lambda x, /: x

    def o(self, f : Lambda[b, c], g : Lambda[a, b], /) -> Lambda[a, c]:
        return lambda x, /: f(g(x))


def arrow(inst : Category[cat], f : hkt[cat, a, b], g : hkt[cat, b, c], /) -> hkt[cat, a, c]:
    return inst.o(g, f)
