import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


class LabMap:
    def __init__(self, data: str):
        self.columns = data.index("\n")
        data = data.replace("\n", "")
        self.rows = len(data) // self.columns
        self.obstacles = set(divmod(i, self.columns) for i, c in enumerate(data) if c == "#")
        self.guard = divmod(data.index("^"), self.columns)
        self.guard_direction = 0

    def step_guard(self):
        step = DIRECTIONS[self.guard_direction]
        new_pos = (self.guard[0] + step[0], self.guard[1] + step[1])
        if new_pos in self.obstacles:
            self.turn_guard()
            return self.step_guard()

        self.guard = new_pos
        return 0 <= self.guard[0] < self.rows and 0 <= self.guard[1] < self.columns

    def turn_guard(self):
        self.guard_direction = (self.guard_direction + 1) % 4

    def has_cycle(self):
        positions = defaultdict(set)
        while self.step_guard():
            if self.guard in positions[self.guard_direction]:
                return True
            positions[self.guard_direction].add(self.guard)
        return False


def parse(data):
    return LabMap(data)


def part_a(data: LabMap):
    positions = set([data.guard])
    while data.step_guard():
        positions.add(data.guard)
    return len(positions)


def part_b(data: LabMap):
    cycle_obstacles = set()
    initial_pos = data.guard

    positions = set([initial_pos])
    while data.step_guard():
        positions.add(data.guard)

    for pos in positions:
        data.guard = initial_pos
        data.guard_direction = 0

        if pos in data.obstacles:
            continue

        data.obstacles.add(pos)
        if data.has_cycle():
            cycle_obstacles.add(pos)
        data.obstacles.remove(pos)

    return len(cycle_obstacles)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day06.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 6 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=6, year=2024)

    print("Running day 6 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=6, year=2024)
