import asyncio
import threading

from os import getpid
from collections import deque
from typing import Any, Callable
from generic_obj import GenericObject
from exceptions import IllegalProcessAccessError


class ObjectPool:
    """
    Synchronous object-pool, imitating Go's (Golang) sync.Pool implementation.
    This is a thread-safe solution for object synchronization across multiple threads,
    with the main goal of minimizing memory related overhead by reusing already allocated memory.

    Attributes:
        cap (int | None): The maximum capacity of objects in the pool. If None, the pool has unlimited capacity.
        obj (Any): The class of objects to be managed by the pool. Defaults to GenericObject.
        on_put (Callable | None): Optional callback function to be executed when an object is put into the pool.
        on_get (Callable | None): Optional callback function to be executed when an object is retrieved from the pool.
    """

    def __init__(
        self,
        max_len: int | None = None,
        obj: Any = None,
        on_put: Callable | None = None,
        on_get: Callable | None = None,
    ) -> None:
        self.stack = deque(maxlen=max_len)
        self.obj = obj or GenericObject
        self.on_put = on_put
        self.on_get = on_get

        self._lock = threading.Lock()
        self._pool_pid = getpid()

    def _validate_process(self) -> None:
        if self._pool_pid != getpid():
            raise IllegalProcessAccessError()

    def count(self) -> int:
        "Returns the number of elements in the stack"
        with self._lock:
            return len(self.stack)

    def empty(self) -> bool:
        "Returns `True` if stack is empty"
        with self._lock:
            return False if self.count() > 0 else True

    def get(self) -> Any:
        "Get an element from the top of the stack (LIFO)"
        self._validate_process()
        with self._lock:
            if len(self.stack) > 0:
                x = self.stack.pop()
            else:
                x = self.obj()
        if self.on_get:
            self.on_get(x)
        return x

    def put(self, x: Any) -> None:
        "Put an element to the top of the stack"
        self._validate_process()
        if self.on_put:
            self.on_put(x)
        with self._lock:
            self.stack.append(x)


class AsyncObjectPool:
    """
    Asynchronous object-pool, imitating Go's (Golang) sync.Pool implementation.
    This solution is used for object synchronization across multiple coroutines (not a thread-safe),
    with the main goal of minimizing memory related overhead by reusing already allocated memory.

    Attributes:
        cap (int | None): The maximum capacity of objects in the pool. If None, the pool has unlimited capacity.
        obj (Any): The class of objects to be managed by the pool. Defaults to GenericObject.
        on_put (Callable | None): Optional callback function to be executed when an object is put into the pool.
        on_get (Callable | None): Optional callback function to be executed when an object is retrieved from the pool.
    """

    def __init__(
        self,
        max_len: int | None = None,
        obj: Any = None,
        on_put: Callable | None = None,
        on_get: Callable | None = None,
    ) -> None:
        self.stack = deque(maxlen=max_len)
        self.obj = obj or GenericObject
        self.on_put = on_put
        self.on_get = on_get

        self._lock = asyncio.Lock()
        self._pool_pid = getpid()

    def _validate_process(self) -> None:
        if self._pool_pid != getpid():
            raise IllegalProcessAccessError()

    async def async_count(self) -> int:
        "Returns the number of elements in the stack"
        async with self._lock:
            return len(self.stack)

    async def async_empty(self) -> bool:
        "Returns `True` if stack is empty"
        return False if await self.async_count() > 0 else True

    async def async_get(self) -> Any:
        "Get() coroutine-safe; Not thread-safe."
        self._validate_process()
        async with self._lock:
            if len(self.stack) > 0:
                x = self.stack.pop()
            else:
                x = self.obj()
        if self.on_get:
            self.on_get(x)
        return x

    async def async_put(self, x: Any) -> None:
        "Put() coroutine-safe; Not thread-safe."
        self._validate_process()
        if self.on_put:
            self.on_put(x)
        async with self._lock:
            self.stack.append(x)
