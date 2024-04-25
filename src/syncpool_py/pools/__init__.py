from os import getpid
from collections import deque
from typing import Any, Callable
from syncpool_py.objects import GenericObject
from syncpool_py.exceptions import IllegalProcessAccessError, PoolClosedError


class BaseObjectPool:
    def __init__(
        self,
        max_len: int | None = None,
        obj: Any = None,
        on_put: Callable | None = None,
        on_get: Callable | None = None,
    ) -> None:
        self.obj = obj or GenericObject
        self.on_put = on_put
        self.on_get = on_get

        self._stack = deque(maxlen=max_len)
        self._running = True
        self._pool_pid = getpid()

    def is_running(self) -> bool:
        return True if self._running else False

    def close(self) -> None:
        if self._running:
            self._running = False
            self._stack.clear()

    def open(self) -> None:
        if not self._running:
            self._running = True

    def clean_pool(self) -> None:
        if len(self._stack) > 0:
            self._stack.clear()

    def _validate_process(self) -> None:
        if self._pool_pid != getpid():
            raise IllegalProcessAccessError()

    def count(self) -> int:
        "Returns the number of elements in the stack"
        return len(self._stack)

    def is_empty(self) -> bool:
        "Returns `True` if stack is empty"
        return False if len(self._stack) > 0 else True

    def get(self) -> Any:
        "Get an element from the top of the stack (LIFO)"
        self._validate_process()
        if self._running:
            if len(self._stack) > 0:
                o = self._stack.pop()
            else:
                o = self.obj()
            if self.on_get:
                self.on_get(o)
            return o
        else:
            raise PoolClosedError()

    def put(self, o: Any) -> None:
        "Put an element to the top of the stack"
        self._validate_process()
        if self._running:
            if self.on_put:
                self.on_put(o)
            self._stack.append(o)
        else:
            raise PoolClosedError()
