from abc import abstractmethod
from typing import TypeVar, Optional
from ode.output import Output

V = TypeVar('V')

class ValueOutput(Output[V]):
    def __init__(self, value: Optional[V] = None):
        super().__init__(value)

    def is_error(self) -> bool:
        return False
