import time
from copy import deepcopy
from itertools import cycle

from aocd import submit

from pyutils import utils

ROCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (0, 1), (1, 0), (1, 1)],
]
JET_MAP = {">": 1, "<": -1}


def parse(data):
    return data


def drop_rock(tower, total_height, rocks_cycle, jet_cycle):
    rock = next(rocks_cycle)
    width = max(coord[0] for coord in rock) + 1

    def is_rock_colliding(left, bottom):
        if left < 0 or left + width > 7 or bottom < 0:
            return True
        for coord in rock:
            if (coord[0] + left, coord[1] + bottom) in tower:
                return True
        return False

    bottom = total_height + 3
    left = 2

    jets = 0
    while True:
        jet = next(jet_cycle)
        jets += 1

        if not is_rock_colliding(left + JET_MAP[jet], bottom):
            left += JET_MAP[jet]

        if is_rock_colliding(left, bottom - 1):
            for coord in rock:
                tower.add((coord[0] + left, coord[1] + bottom))
                total_height = max(total_height, coord[1] + bottom + 1)
            break
        else:
            bottom -= 1

    return total_height, jets


def part_a(data):
    rocks_cycle = cycle(ROCKS)
    jet_cycle = cycle(data)

    tower = set()
    total_height = 0
    for _ in range(2022):
        total_height, _ = drop_rock(tower, total_height, rocks_cycle, jet_cycle)

    return total_height


def part_b(data):
    rocks_cycle = cycle(ROCKS)
    jet_cycle = cycle(data)

    tower = set()
    total_height = 0
    r = 0
    j = 0
    cache = {}
    for i in range(1000000000000):
        if (r, j) in cache:
            prev_i, height_i = cache[(r, j)]
            cycles, rem = divmod(1000000000000 - i, i - prev_i)
            if rem == 0:
                return total_height + (total_height - height_i) * cycles
        else:
            cache[(r, j)] = i, total_height

        total_height, jets = drop_rock(tower, total_height, rocks_cycle, jet_cycle)
        r = (r + 1) % len(ROCKS)
        j = (j + jets) % len(data)

    return -1


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day17.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 17 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=17, year=2022)

    print("Running day 17 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=17, year=2022)
