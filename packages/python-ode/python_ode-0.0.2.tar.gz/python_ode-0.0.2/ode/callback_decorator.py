from ode.error_output import ErrorOutput
from ode.use_case import UseCase
from ode.output import Output
from ode.use_case_decorator import UseCaseDecorator
from typing import Callable, TypeVar

P = TypeVar('P')
R = TypeVar('R')

class CallbackDecorator(UseCaseDecorator[P, R]):
    
    def __init__(self, use_case: UseCase[P, R], callback: Callable[[Output[R]], None]):
        self.callback = callback
        use_case.on_result = lambda output : { callback(output) }
        use_case.on_error = lambda error : { callback(ErrorOutput(error))}
        super().__init__(use_case)