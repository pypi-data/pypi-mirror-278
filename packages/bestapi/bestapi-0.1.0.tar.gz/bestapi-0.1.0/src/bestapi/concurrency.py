from __future__ import annotations

import asyncio
import typing as t

T = t.TypeVar("T")


class _StopIteration(Exception):
    pass


def _next(iterator: t.Iterator[T]) -> T:
    # We can't raise `StopIteration` from within the threadpool iterator
    # and catch it outside that context, so we coerce them into a different
    # exception type.
    try:
        return next(iterator)
    except StopIteration:
        raise _StopIteration


async def iterate_in_threadpool(iterator: t.Iterable[T]) -> t.AsyncIterator[T]:
    as_iterator = iter(iterator)
    while True:
        try:
            yield await asyncio.to_thread(_next, as_iterator)
        except _StopIteration:
            break
