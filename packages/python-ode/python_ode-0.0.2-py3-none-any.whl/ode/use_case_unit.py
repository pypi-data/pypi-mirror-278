from typing import TypeVar, Generic, Optional
from ode.callback_decorator import CallbackDecorator
from ode.output import Output
from ode.value_out_put import ValueOutput

from ode.use_case import UseCase

P = TypeVar('P')
R = TypeVar('R')

class UseCaseUnit(Generic[P, R]):
    def __init__(self, use_case: UseCase[P, R], param: Optional[P] = None):
        self.use_case = use_case
        self.param = param

    def process(self) -> Output[R]:
        callback = self.Callback()
        decorator = CallbackDecorator(self.use_case, callback.set)
        decorator.process(self.param)
        return callback.output

    class Callback:
        def __init__(self):
            self.output = ValueOutput()

        def set(self, value: Output[R]):
            self.output = value
