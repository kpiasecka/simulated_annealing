from __future__ import annotations

from random import randint
import numpy as np


class ProblemInstance:
    def __init__(self, times: list):
        self._times = np.array(times)

    @property
    def machines(self) -> int:
        return self._times.shape[0]

    @property
    def tasks(self) -> int:
        return self._times.shape[1]

    @property
    def times(self) -> np.array:
        return self._times

    @staticmethod
    def generate(tasks: int, machines: int) -> ProblemInstance:
        times = [[randint(1, 99) for _ in range(tasks)] for __ in range(machines)]

        return ProblemInstance(times)
