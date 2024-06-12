from abc import ABC, abstractmethod
from typing import Any, Callable

class Controller(ABC):
    @abstractmethod
    def observe(self, channel_name: str, listener: Callable[[Any], None]):
        pass