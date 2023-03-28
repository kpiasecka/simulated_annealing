from random import randint


def generate_instance(machines_no: int, tasks_no: int):
    return [[randint(1, 99) for _ in range(tasks_no)] for __ in range(machines_no)]

