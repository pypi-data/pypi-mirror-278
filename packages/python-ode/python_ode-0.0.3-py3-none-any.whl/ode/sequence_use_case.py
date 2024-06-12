from typing import TypeVar, List, Optional
from ode.use_case import UseCase
from ode.output import Output
from ode.value_out_put import ValueOutput
from ode.use_case_unit import UseCaseUnit

P = TypeVar('P')
R = TypeVar('R')
T = TypeVar('T')


class SequenceUseCase(UseCase[None, List[Output]]):
    def __init__(self, units: List[UseCaseUnit]):
        self.units = units
        self.stream: List[Output] = []

    @classmethod
    def builder(cls) -> 'SequenceUseCase.Builder':
        return cls.Builder()

    async def execute(self, param: Optional[None] = None) -> Output[List[Output]]:
        for unit in self.units:
            output = await unit.process()
            self.stream.append(output)

        return ValueOutput(self.stream)

    class Builder:
        def __init__(self):
            self.list: List[UseCaseUnit] = []

        def add(self, use_case: UseCase[P, R], param: Optional[P] = None) -> 'SequenceUseCase.Builder':
            self.list.append(UseCaseUnit(use_case, param))
            return self

        def build(self) -> UseCase[None, List[Output]]:
            return SequenceUseCase(self.list)
