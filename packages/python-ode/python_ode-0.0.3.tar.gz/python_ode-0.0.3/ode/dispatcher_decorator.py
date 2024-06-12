import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional, TypeVar, Generic

from ode.output import Output
from ode.use_case import UseCase
from ode.use_case_decorator import UseCaseDecorator

P = TypeVar('P')
R = TypeVar('R')


class UseCaseDispatcher(Generic[P, R]):
    def __init__(self, use_case: UseCase[P, R], loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.decorator = UseCaseDispatcher.DispatcherDecorator(use_case, self.loop)

    async def dispatch(self, param: Optional[P] = None) -> asyncio.Task:
        return await self.decorator.dispatch(param)

    class DispatcherDecorator(UseCaseDecorator[P, R]):
        def __init__(self, use_case: UseCase[P, R], loop: asyncio.AbstractEventLoop):
            super().__init__(use_case)
            self.loop = loop

        async def dispatch(self, param: Optional[P] = None) -> asyncio.Task:
            return await self.loop.create_task(self.use_case.process(param))

        async def on_result(self, output: Output[R] = None):
            return await self.loop.create_task(self.use_case.on_result(output))

        async def on_error(self, error: Exception):
            return await self.loop.create_task(self.use_case.on_error(error))
