from typing import Generic, Optional, TypeVar

T = TypeVar("T")


def unwrap(val: Optional[T]) -> T:
    """
    Unwrap a value from an Optional
    """
    if val is None:
        raise ValueError("Value is None")
    return val


class Option(Generic[T]):
    def __init__(self, val: Optional[T] = None):
        self._val = val

    def unwrap(self) -> T:
        if self._val is None:
            raise ValueError("None")
        return self._val

    def is_some(self) -> bool:
        return self._val is not None

    @property
    def val(self) -> Optional[T]:
        return self._val

    @val.setter
    def val(self, val: Optional[T]):
        self._val = val
