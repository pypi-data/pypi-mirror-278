from typing import Optional, TypeVar

from ode.authentication_exception import AuthenticationException
from ode.dispatcher_decorator import UseCaseDispatcher
from ode.http_exception import HttpException
from ode.internet_connection_exception import InternetConnectionException
from ode.use_case import UseCase
from ode.callback_decorator import CallbackDecorator

from ode.composite_job_disposable import CompositeJobDisposable
from ode.output import Output

from ode.use_case_unit import UseCaseUnit

P = TypeVar('P')
R = TypeVar('R')

class BaseController:
    composite_job_disposable: Optional[CompositeJobDisposable] = None

    def handle_response(self, state):
        if self.is_error(state):
            self.handle_throwable(state.error)
        else:
            self.handle_success(state.value)

    def is_error(self, state):
        return state.is_error()

    def handle_throwable(self, error):
        if isinstance(error, AuthenticationException):
            self.handle_auth_error()
        elif isinstance(error, HttpException):
            self.handle_http_error(error)
        elif isinstance(error, InternetConnectionException):
            self.handle_connection_error()
        else:
            self.handle_error(error)

    def handle_auth_error(self):
        pass

    def handle_http_error(self, error):
        pass

    def handle_connection_error(self):
        pass

    def handle_error(self, error: Exception):
        pass

    def handle_success(self, value):
        pass

    def dispatch_use_case(self, param: P, use_case: UseCase[P, R]) -> any:
        dispatcher = UseCaseDispatcher(use_case, CallbackDecorator(use_case, callback=lambda output: self.handle_response(output)))
        job = dispatcher.dispatch(param)
        if self.composite_job_disposable:
            self.composite_job_disposable.add(job)
        
        return job
    
    def process_use_case(self, param: P, use_case: UseCase[P, R]) -> Output[R]:
        callback = UseCaseUnit.Callback()
        CallbackDecorator(use_case, callback.set).process(param)

        return callback.output