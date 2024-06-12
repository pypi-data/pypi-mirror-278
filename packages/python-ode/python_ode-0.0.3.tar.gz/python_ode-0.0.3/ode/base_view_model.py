import asyncio
from typing import Any, Callable, Dict, List, Optional, TypeVar

from ode.callback_decorator import CallbackDecorator
from ode.composite_job_disposable import CompositeJobDisposable
from ode.controller import Controller
from ode.dispatcher_decorator import UseCaseDispatcher
from ode.output import Output
from ode.use_case import UseCase

P = TypeVar('P')
R = TypeVar('R')

class BaseViewModel:
    def __init__(self):
        self.channels: Dict[str, List[Callable[[Any], None]]] = {}
        self.composite_job_disposable = CompositeJobDisposable()

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

    def dispatch_use_case(self, param: Optional[P], use_case: UseCase[P, R], listener: Callable[[Output[R]], None]) -> asyncio.Task:
        dispatcher = UseCaseDispatcher(CallbackDecorator(use_case, listener))
        job = dispatcher.dispatch(param)
        self.composite_job_disposable.add(job)
        return job