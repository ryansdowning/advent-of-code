import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils


class ZeroRock:
    def __init__(self):
        self.step = 0
        self.count = 1

    def update(self):
        if self.step == 5:
            return [Rock(4048), Rock(1), Rock(4048), Rock(8096)]

        if self.step == 0:
            # Represents 1
            pass
        elif self.step == 1:
            # Reperesents 2024
            pass
        elif self.step == 2:
            # Represents 20 and 24
            self.count = 2
        elif self.step == 3:
            # Represents 2 0 2 4
            self.count = 4
        elif self.step == 4:
            # Represents 4048 1 4048 8096
            pass

        self.step += 1
        return [self]


class Rock:
    def __init__(self, value: int):
        self.value = value
        self.count = 1

    def update(self):
        new_values = update_rock(self.value)
        return [Rock(new_value) if new_value else ZeroRock() for new_value in new_values]


def update_rock(value: int) -> tuple[int] | tuple[int, int]:
    if value == 0:
        return (1,)
    if (str_len := len((str_val := str(value)))) % 2 == 0:
        idx = str_len // 2
        return int(str_val[:idx]), int(str_val[idx:])
    return (value * 2024,)


def update_rocks(rocks: dict[int, int]) -> dict[int, int]:
    new_rocks = rocks.copy()
    for value, count in rocks.items():
        new_values = update_rock(value)
        for new_value in new_values:
            new_rocks[new_value] += count
        new_rocks[value] -= count
    return new_rocks


def solve(data, n):
    rocks = defaultdict(int)
    for rock in data:
        rocks[rock] += 1

    for _ in range(n):
        rocks = update_rocks(rocks)

    return sum(rocks.values())


def parse(data):
    return list(map(int, data.split(" ")))


def part_a(data):
    return solve(data, 25)


def part_b(data):
    return solve(data, 75)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day11.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 11 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=11, year=2024)

    print("Running day 11 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=11, year=2024)
