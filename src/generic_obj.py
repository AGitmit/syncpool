from typing import Any


class GenericObject:
    def __init__(self) -> None:
        self.value: Any = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} w/ value of '{self.value}' of type {type(self.value)}"
