from __future__ import annotations

import math
from abc import ABC, abstractmethod
from .flow_shop import ProblemInstance
import numpy as np
from random import choice
from pandas import DataFrame
import plotly.figure_factory as ff


class StopCondition(ABC):
    @abstractmethod
    def should_stop(self) -> bool:
        raise NotImplemented

    def __str__(self) -> str:
        return self.__class__.__name__


class IterativeCondition(StopCondition):
    def __init__(self, n: int):
        self.n = n
        self.i = 0  # iteration

    def should_stop(self) -> bool:
        if self.i == self.n:
            return True
        self.i += 1
        return False


class Criteria(ABC):
    @abstractmethod
    def get_value(self, problem_instance: ProblemInstance, solution: np.array) -> int:
        raise NotImplemented

    def __str__(self) -> str:
        return self.__class__.__name__

    @staticmethod
    def calculate_times(problem_instance: ProblemInstance, solution: np.array) -> np.array:
        machines_times = []
        for machine in range(problem_instance.times.shape[0]):
            machines_times.append([])
            for task, task_id in enumerate(solution):
                task_time = problem_instance.times[machine][task_id]
                if machine == 0 and task == 0:
                    machines_times[machine].append(task_time)
                elif machine == 0 and task > 0:
                    previous_time = machines_times[machine][task - 1]
                    machines_times[machine].append(previous_time + task_time)
                elif machine > 0 and task == 0:
                    previous_machine_time = machines_times[machine - 1][task]
                    machines_times[machine].append(previous_machine_time + task_time)
                else:
                    previous_machine_time = machines_times[machine - 1][task]
                    previous_time = machines_times[machine][task - 1]
                    machines_times[machine].append(max(previous_machine_time, previous_time) + task_time)
        return np.array(machines_times)


class MakeSpan(Criteria):
    def get_value(self, problem_instance: ProblemInstance, solution: np.array) -> int:
        times = self.calculate_times(problem_instance, solution)

        return times[problem_instance.machines - 1][problem_instance.tasks - 1]


class FlowTime(Criteria):
    def get_value(self, problem_instance: ProblemInstance, solution: np.array) -> int:
        times = self.calculate_times(problem_instance, solution)

        return np.sum(times, axis=1)[-1]


class Cooling(ABC):
    @abstractmethod
    def cool_down(self, temp: float) -> float:
        raise NotImplemented

    def __str__(self) -> str:
        return self.__class__.__name__


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
    def __init__(
            self,
            temp: float,
            cooling: Cooling,
            stop_condition: StopCondition,
            criteria: Criteria,
            problem_instance: ProblemInstance
    ):
        self.temp = temp
        self.cooling = cooling
        self.stop_condition = stop_condition
        self.criteria = criteria
        self.best_solution = np.array([])
        self._problem_instance = problem_instance

    def solve(self) -> np.array:
        self.get_random_solution(self._problem_instance.tasks)
        print(f"Starting temp: {self.temp}")
        print(f"Cooling pattern: {self.cooling}")
        print(f"Stop condition: {self.stop_condition}")
        print(f"Starting best solution: {self.best_solution}\n")
        while not self.stop_condition.should_stop():
            next_solution = self.move(self.best_solution)
            if self.should_accept(next_solution):
                self.best_solution = next_solution
                print(f"Current best solution: {self.best_solution}")
            self.temp = self.cooling.cool_down(self.temp)
            print(f"Current temp: {self.temp}\n")
        print("#### END ####")
        return self.best_solution

    def plot(self) -> None:
        times = self.criteria.calculate_times(self._problem_instance, self.best_solution)
        title = f"{self.criteria} value for task permutation: {[i + 1 for i in self.best_solution]} is" \
                f" {self.criteria.get_value(self._problem_instance, self.best_solution)}"
        gantt = []
        for machine in range(self._problem_instance.machines):
            for task, task_id in enumerate(self.best_solution):
                start = 0
                end = times[machine][task]
                if machine == 0 and task > 0:
                    start = times[machine][task - 1]
                elif machine > 0 and task == 0:
                    start = times[machine-1][task]
                elif machine > 0 and task > 0:
                    previous_task = times[machine][task - 1]
                    previous_machine_task = times[machine - 1][task]
                    start = max(previous_task, previous_machine_task)
                gantt.append(
                    dict(
                        Task=f"Machine {machine+1}",
                        Start=start,
                        Finish=end,
                        Id=f"Task {task_id+1}"
                    )
                )
        fig = ff.create_gantt(
            df=DataFrame(gantt),
            title=title,
            bar_width=.4,
            index_col="Id",
            show_colorbar=True,
            group_tasks=True
        )
        fig.update_layout(xaxis_type="linear")
        fig.show()

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
        best_solution_value = self.criteria.get_value(self._problem_instance, self.best_solution)
        next_solution_value = self.criteria.get_value(self._problem_instance, next_solution)

        if next_solution_value < best_solution_value:
            return True  # its better
        else:
            probability = math.exp(-(next_solution_value - best_solution_value) / self.temp)
            accepted = np.random.rand() <= probability
            print(f"Found worse solution. Probability of accepting: {probability * 100:.2f}%\nAccepted: {accepted}")

            return accepted
