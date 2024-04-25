import threading

from typing import Callable, Any
from syncpool_py.pools import BaseObjectPool


class SyncObjectPool(BaseObjectPool):
    """
    Synchronous object-pool, imitating Go's (Golang) sync.Pool implementation.
    This is a thread-safe solution for object synchronization across multiple threads,
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
        self._lock = threading.Lock()

    def _with_lock(func: Callable):
        def wrapper(self, *args, **kwargs):
            with self._lock:
                result = func(self, *args, **kwargs)
            return result

        return wrapper

    @_with_lock
    def close(self) -> None:
        return super().close()

    @_with_lock
    def open(self) -> None:
        return super().open()

    @_with_lock
    def clean_pool(self) -> None:
        return super().clean_pool()

    @_with_lock
    def count(self) -> int:
        return super().count()

    @_with_lock
    def is_empty(self) -> bool:
        return super().is_empty()

    @_with_lock
    def get(self) -> Any:
        return super().get()

    @_with_lock
    def put(self, o: Any) -> None:
        return super().put(o)
