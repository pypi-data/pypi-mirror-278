from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Generic

V = TypeVar('V')


class Output(Generic[V]):
    def __init__(self, value: Optional[V] = None, error: Optional[Exception] = None):
        self.value = value
        self.error = error

    def is_error(self) -> bool:
        return self.error is not None

    def is_success(self) -> bool:
        return not self.is_error()

    def is_empty(self) -> bool:
        return self.value is None
