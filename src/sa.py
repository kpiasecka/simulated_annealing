from __future__ import annotations

import math
from abc import ABC, abstractmethod
from flow_shop import ProblemInstance
import numpy as np
from random import choice


class StopCondition(ABC):
    @abstractmethod
    def should_stop(self) -> bool:
        raise NotImplemented


class IterativeCondition(StopCondition):
    def __init__(self, n: int):
        self.n = n
        self.i = 0  # iteration

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
    def __init__(self, alpha: float):
        self.alpha = alpha

    def cool_down(self, temp: float) -> float:
        return temp * self.alpha


class LinearCooling(Cooling):
    def __init__(self, beta: float):
        self.beta = beta

    def cool_down(self, temp: float) -> float:
        return temp - self.beta


class SA:
    def __init__(self, temp: float, cooling: Cooling, stop_condition: StopCondition, criteria: Criteria):
        self.temp = temp
        self.cooling = cooling
        self.stop_condition = stop_condition
        self.criteria = criteria
        self.best_solution = np.array([])

    def solve(self, problem_instance: ProblemInstance) -> np.array:
        self.get_random_solution(problem_instance.tasks)
        while not self.stop_condition.should_stop():
            next_solution = self.move(self.best_solution)
            if self.should_accept(next_solution):
                self.best_solution = next_solution
            self.temp = self.cooling.cool_down(self.temp)
        return self.best_solution

    def get_random_solution(self, tasks: int) -> None:
        self.best_solution = np.random.permutation(tasks)

    @staticmethod
    def move(best_solution: np.array) -> np.array:
        first_task = np.random.randint(0, len(best_solution))
        left_tasks = [i for i in range(len(best_solution)) if i != first_task]
        second_task = choice(left_tasks)
        new_solution = best_solution.copy()
        new_solution[first_task], new_solution[second_task] = new_solution[second_task], new_solution[first_task]
        return new_solution

    def should_accept(self, next_solution: np.array) -> bool:
        best_solution_value = self.criteria.get_value(self.best_solution)
        next_solution_value = self.criteria.get_value(next_solution)

        if next_solution_value < best_solution_value:
            return True  # its better
        else:
            probability = math.exp(-(next_solution_value - best_solution_value) / self.temp)
            return np.random.rand() <= probability
