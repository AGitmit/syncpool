import time

from os import getpid
from collections import deque
from typing import Any, Callable
from syncpool_py.objects import GenericObject
from syncpool_py import exceptions

# TODO: finish implementing object's lifespan logic


class BaseObjectPool:
    def __init__(
        self,
        max_len: int | None = None,
        obj: Any = None,
        on_put: Callable | None = None,
        on_get: Callable | None = None,
        # obj_lifespan: int | None = None,
    ) -> None:
        self.obj = obj or GenericObject
        self.on_put = on_put
        self.on_get = on_get
        # self.obj_lifespan = obj_lifespan

        self._stack = deque(maxlen=max_len)
        self._running = True
        self._pool_pid = getpid()

    def _allow_when_running(func: Callable):
        "Allows a function to run only if pool is open and running."

        def wrapper(self, *args, **kwargs):
            if self._running:
                return func(self, *args, **kwargs)
            raise exceptions.PoolClosedError()

        return wrapper

    def _validate_owner_process(func: Callable):
        """
        Validate owner process for operations performed on the pool.
        A pool should only be shared from within it's owner process.
        """

        def wrapper(self, *args, **kwargs):
            if self._pool_pid != getpid():
                raise exceptions.IllegalProcessAccessError()
            return func(self, *args, **kwargs)

        return wrapper

    def _peekleft_clean_on_expire(self) -> None:
        """
        *Not implemented yet*
        Cleans expired objects from the stack.
        Expired objects are objects which lifespan has surpassed the declared lifespan value (if declared).
        """
        # peekleft = self._stack[0] if self._stack else None
        # if peekleft:
        #     timestamp = peekleft[1]
        #     if timestamp >= self.obj_lifespan:
        #         self._stack.popleft()
        ...

    @_validate_owner_process
    def is_running(self) -> bool:
        return True if self._running else False

    @_validate_owner_process
    @_allow_when_running
    def close(self) -> None:
        "Closes the pool and freezes the stack at it's current state"
        self._running = False

    @_validate_owner_process
    def open(self) -> None:
        "Re-opens the pool. Does nothing if the pool is already open"
        if not self._running:
            self._running = True

    @_validate_owner_process
    def clean_pool(self) -> None:
        "Resets the stack from objects"
        if len(self._stack) > 0:
            self._stack.clear()

    @_validate_owner_process
    def count(self) -> int:
        "Returns the number of elements in the stack"
        return len(self._stack)

    @_validate_owner_process
    def is_empty(self) -> bool:
        "Returns `True` if stack is empty"
        return False if len(self._stack) > 0 else True

    @_validate_owner_process
    @_allow_when_running
    def get(self) -> Any:
        "Gets an element from the top of the stack (LIFO - last in, first out)"
        self._validate_owner_process()
        if len(self._stack) > 0:
            o, _ = self._stack.pop()  # drop timestamp
            if self.on_get:
                self.on_get(o)
            return o
        return None

    @_validate_owner_process
    @_allow_when_running
    def get_new_obj(self) -> Any:
        return self.obj()

    @_validate_owner_process
    @_allow_when_running
    def put(self, o: Any) -> None:
        "Puts an element to the top of the stack"
        if not self._stack.maxlen or self._stack.maxlen > len(self._stack):
            if self.on_put:
                self.on_put(o)
            return self._stack.append((o, time.time()))  # include timestamp of insertion
        raise exceptions.PoolCapacityReachedError()
