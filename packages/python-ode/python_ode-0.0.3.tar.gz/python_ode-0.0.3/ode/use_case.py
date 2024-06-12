from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional
from ode.output import Output
from ode.error_output import ErrorOutput

P = TypeVar('P')
R = TypeVar('R')


class UseCase(ABC, Generic[P, R]):

    async def process(self, param: Optional[P] = None):
        try:
            if self.guard(param):
                output = await self.execute(param)
                await self.on_result(output)
            else:
                await self.on_guard_error()
        except Exception as error:
            await self.on_error(error)

    async def execute(self, param: Optional[P] = None) -> Output[R]:
        pass

    async def on_error(self, error: Exception):
        await self.on_result(ErrorOutput(error))

    async def on_result(self, output: Output[R] = None):
        pass

    def guard(self, param: Optional[P] = None) -> bool:
        return True

    async def on_guard_error(self):
        pass
