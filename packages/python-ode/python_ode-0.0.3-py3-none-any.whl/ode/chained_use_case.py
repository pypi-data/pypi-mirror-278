from typing import TypeVar, Optional
from ode.use_case import UseCase
from ode.output import Output
from ode.error_output import ErrorOutput

P = TypeVar('P')
R = TypeVar('R')
T = TypeVar('T')


class ChainedUseCase(UseCase[P, T]):
    def __init__(self, first: UseCase[P, R], second: UseCase[R, T]):
        self.first = first
        self.second = second

    async def execute(self, param: Optional[P] = None) -> Output[T]:
        intermediate = await self.first.execute(param)
        if intermediate.is_success():
            return await self.second.execute(intermediate.value)
        return ErrorOutput(intermediate.error)
