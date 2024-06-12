from ode.error_output import ErrorOutput
from ode.use_case import UseCase
from ode.output import Output
from ode.use_case_decorator import UseCaseDecorator
from typing import Callable, TypeVar, Optional, Awaitable

P = TypeVar('P')
R = TypeVar('R')


class CallbackDecorator(UseCaseDecorator[P, R]):
    def __init__(self, use_case: UseCase[P, R], callback: Callable[[Output[R]], Awaitable[None]]):
        super().__init__(use_case)
        self.callback = callback

    async def on_result(self, output: Output[R] = None):
        await self.use_case.on_result(output)
        await self.callback(output)

    async def on_error(self, error: Exception):
        await self.callback(ErrorOutput(error))
        await self.use_case.on_error(error)

