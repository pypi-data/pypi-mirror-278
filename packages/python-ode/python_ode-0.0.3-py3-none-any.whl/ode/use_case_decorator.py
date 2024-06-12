from abc import abstractmethod
from typing import TypeVar, Optional
from ode.use_case import UseCase
from ode.output import Output

P = TypeVar('P')
R = TypeVar('R')


class UseCaseDecorator(UseCase[P, R]):
    def __init__(self, use_case: UseCase[P, R]):
        self.use_case = use_case

    async def execute(self, param: Optional[P] = None) -> Output[R]:
        return await self.use_case.execute(param)

    async def on_result(self, output: Output[R] = None):
        return await self.use_case.on_result(output)

    async def on_error(self, error: Exception):
        return await self.use_case.on_error(error)

    def guard(self, param: Optional[P] = None) -> bool:
        return self.use_case.guard(param)
