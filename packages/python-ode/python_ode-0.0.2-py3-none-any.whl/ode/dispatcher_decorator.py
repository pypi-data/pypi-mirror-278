import threading
from ode.use_case_decorator import UseCaseDecorator

class UseCaseDispatcher:
    def __init__(self, use_case, execute_on=None):
        self.decorator = DispatcherDecorator(use_case, execute_on)

    def dispatch(self, param=None):
        return self.decorator.dispatch(param)

class DispatcherDecorator(UseCaseDecorator):
    def __init__(self, use_case, result_on=None):
        super().__init__(use_case)
        self.result_on = result_on

    def dispatch(self, param=None):
        threading.Thread(target=self.process(param=param)).start()

    def on_error(self, error):
        threading.Thread(target=self.use_case.on_error(error)).start()

    def on_result(self, output):
        threading.Thread(target=self.use_case.on_result(output))