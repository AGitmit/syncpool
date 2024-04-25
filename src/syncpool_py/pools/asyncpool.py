import asyncio

from typing import Any, Callable
from syncpool_py.pools import BaseObjectPool


class AsyncObjectPool(BaseObjectPool):
    """
    Asynchronous object-pool, imitating Go's (Golang) sync.Pool implementation.
    This solution is used for object synchronization across multiple coroutines (not a thread-safe),
    with the main goal of minimizing memory related overhead by reusing already allocated memory.

    Attributes:
        cap (int | None): The maximum capacity of objects in the pool. If None, the pool has unlimited capacity.
        obj (Any): The class of objects to be managed by the pool. Defaults to GenericObject.
        on_put (Callable | None): Optional callback function to be executed when an object is put into the pool.
        on_get (Callable | None): Optional callback function to be executed when an object is retrieved from the pool.
        Callbacks should return `None` and only perform operations on the object itself;
        Any further processing on the object shall occur after getting it from the pool or before putting it back.
    """

    def __init__(
        self,
        max_len: int | None = None,
        obj: Any = None,
        on_put: Callable[..., Any] | None = None,
        on_get: Callable[..., Any] | None = None,
    ) -> None:
        super().__init__(max_len, obj, on_put, on_get)
        self._lock = asyncio.Lock()

    def _with_lock(func: Callable):
        async def wrapper(self, *args, **kwargs):
            async with self._lock:
                return await func(self, *args, **kwargs)

        return wrapper

    @_with_lock
    async def close(self) -> None:
        return super().close()

    @_with_lock
    async def open(self) -> None:
        return super().open()

    @_with_lock
    async def clean_pool(self) -> None:
        return super().clean_pool()

    @_with_lock
    async def count(self) -> int:
        return super().count()

    @_with_lock
    async def is_empty(self) -> bool:
        return super().is_empty()

    @_with_lock
    async def get(self) -> Any:
        return super().get()

    @_with_lock
    async def put(self, o: Any) -> None:
        return super().put(o)
