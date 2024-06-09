from typing import TypeVar, List, Optional
from ode.use_case import UseCase
from ode.output import Output
from ode.value_out_put import ValueOutput
from ode.use_case_unit import UseCaseUnit

P = TypeVar('P')
R = TypeVar('R')
T = TypeVar('T')

class SequenceUseCase(UseCase[None, List[Output[T]]]):
    def __init__(self, units: List[UseCaseUnit[P, T]]):
        self.units = units

    def execute(self, param: None = None) -> Output[List[Output[T]]]:
        stream = []
        for unit in self.units:
            output = unit.process()
            stream.append(output)

        return ValueOutput(stream)

    @staticmethod
    def builder():
        return SequenceUseCase.Builder()

    class Builder:
        def __init__(self):
            self.list = []

        def add(self, use_case: UseCase[P, R], param: Optional[P] = None):
            self.list.append(UseCaseUnit(use_case, param))
            return self

        def build(self):
            return SequenceUseCase(self.list)
