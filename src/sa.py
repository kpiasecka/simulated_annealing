from __future__ import annotations
from abc import ABC, abstractmethod


class StopCondition(ABC):
    @abstractmethod
    def should_stop(self) -> bool:
        raise NotImplemented


class Criteria(ABC):
    @abstractmethod
    def get_value(self) -> int:
        raise NotImplemented


class Cooling(ABC):
    @abstractmethod
    def cool_down(self, temp: float) -> float:
        raise NotImplemented


class IterativeCondition(StopCondition):
    def __init__(self, n: int):
        self.n = n
        self.i = 0   # iteration

    def should_stop(self) -> bool:
        self.i += 1
        if self.i == self.n:
            return True
        return False


class SA:
    def __int__(self, temp: float, cooling: Cooling, stop_condition: StopCondition, ):
        self.temp = temp
        self.cooling = cooling
        self.stop_condition = stop_condition

    def solve(self, problem_instance: []):
        pass
