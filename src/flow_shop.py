from __future__ import annotations

from random import randint
from typing import List, Optional
import numpy as np


class ProblemInstance:
    def __init__(self, machines: int, tasks: int, times: Optional[np.array] = None):
        self.machines = machines
        self.tasks = tasks
        self._times = times if not None else np.empty((machines, tasks))

    @property
    def times(self) -> np.array:
        return self._times

    @staticmethod
    def generate(tasks: int, machines: int) -> ProblemInstance:
        times = [[randint(1, 99) for _ in range(tasks)] for __ in range(machines)]

        return ProblemInstance(machines, tasks, times)
