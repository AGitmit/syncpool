import asyncio
import threading

from collections import deque
from typing import Any
from generic_obj import GenericObject


class ObjectPool:
    """
    Sync object-pool, imitating Go's (Golang) sync.Pool implementation.
    This is a thread-safe solution for object synchronization across multiple threads,
    with the main goal of minimizing memory related overhead by reusing already allocated memory.

    Attributes:
        - size (int | None) : set a maximum objects capacity on the stack.
        - obj (Any) : an object class of any type - will be used as a default object to instanciate when stack is empty.
    """

    def __init__(self, cap: int | None = None, obj: Any = None) -> None:
        self.stack = deque(maxlen=cap)
        self.obj = obj or GenericObject
        self._lock = threading.Lock()

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
        with self._lock:
            if self.count() > 0:
                return self.stack.pop()
            return self.obj()

    def put(self, x: Any) -> None:
        "Put an element to the top of the stack"
        with self._lock:
            self.stack.append(x)


class AsyncObjectPool:
    """
    Sync object-pool, imitating Go's (Golang) sync.Pool implementation.
    This solution is used for object synchronization across multiple coroutines (not a thread-safe),
    with the main goal of minimizing memory related overhead by reusing already allocated memory.

    Attributes:
        - size (int | None) : set a maximum objects capacity on the stack.
        - obj (Any) : an object class of any type - will be used as a default object to instanciate when stack is empty.
    """

    def __init__(self, cap: int | None = None, obj: Any = None) -> None:
        self.stack = deque(maxlen=cap)
        self.obj = obj or GenericObject
        self._lock = asyncio.Lock()

    async def async_count(self) -> int:
        "Returns the number of elements in the stack"
        async with self._lock:
            return len(self.stack)

    async def async_empty(self) -> bool:
        "Returns `True` if stack is empty"
        return False if await self.async_count() > 0 else True

    async def async_get(self) -> Any:
        "Get() coroutine-safe; Mot thread-safe."
        if await self.async_count() > 0:
            async with self._lock:
                return self.stack.pop()
        return self.obj()

    async def async_put(self, x: Any) -> None:
        "Put() coroutine-safe; Mot thread-safe."
        async with self._lock:
            self.stack.append(x)
