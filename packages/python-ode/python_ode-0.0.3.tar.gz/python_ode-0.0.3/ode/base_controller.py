import asyncio
from asyncio import Task
from typing import Any, Callable, Dict, List, Optional, TypeVar, Awaitable, Coroutine

from ode.authentication_exception import AuthenticationException
from ode.controller import Controller
from ode.dispatcher_decorator import UseCaseDispatcher
from ode.http_exception import HttpException
from ode.internet_connection_exception import InternetConnectionException
from ode.use_case import UseCase
from ode.callback_decorator import CallbackDecorator

from ode.composite_job_disposable import CompositeJobDisposable
from ode.output import Output

# from ode.use_case_unit import UseCaseUnit

P = TypeVar('P')
R = TypeVar('R')


class BaseController:
    channels: Dict[str, List[Callable[[Any], None]]] = {}
    composite_job_disposable = CompositeJobDisposable()

    def observe(self, channel_name: str, listener: Callable[[Any], None]):
        if channel_name not in self.channels:
            self.channels[channel_name] = []
        self.channels[channel_name].append(listener)

    def get_channels(self) -> List[str]:
        return list(self.channels.keys())

    def dispose_all(self):
        self.composite_job_disposable.cancel()

    def post_value(self, channel_name: str, value: Any):
        if channel_name in self.channels:
            for listener in self.channels[channel_name]:
                listener(value)

    async def dispatch_use_case(self, param: Optional[P], use_case: UseCase[P, R],
                                listener: Callable[[Output[R]], Awaitable[None]]) -> Coroutine[Any, Any, Task]:
        dispatcher = UseCaseDispatcher(CallbackDecorator(use_case, listener))
        job = await dispatcher.dispatch(param)
        # self.composite_job_disposable.add(job)
        return job
