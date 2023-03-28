from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


ProblemInstance = List[List[int]]


class StopCondition(ABC):
    @abstractmethod
    def should_stop(self) -> bool:
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


class Criteria(ABC):
    @abstractmethod
    def get_value(self, problem_instance: ProblemInstance) -> int:
        raise NotImplemented


class MakeSpan(Criteria):
    def get_value(self, problem_instance: ProblemInstance) -> int:
        pass


class FlowTime(Criteria):
    def get_value(self, problem_instance: ProblemInstance) -> int:
        pass


class Cooling(ABC):
    @abstractmethod
    def cool_down(self, temp: float) -> float:
        raise NotImplemented


class GeometricCooling(Cooling):
    def __int__(self, alpha: float):
        self.alpha = alpha

    def cool_down(self, temp: float) -> float:
        return temp * self.alpha


class LinearCooling(Cooling):
    def __int__(self, beta: float):
        self.beta = beta

    def cool_down(self, temp: float) -> float:
        return temp - self.beta


class SA:
    def __int__(self, temp: float, cooling: Cooling, stop_condition: StopCondition, criteria: Criteria):
        self.temp = temp
        self.cooling = cooling
        self.stop_condition = stop_condition
        self.criteria = criteria

    def solve(self, problem_instance: ProblemInstance):
        pass

