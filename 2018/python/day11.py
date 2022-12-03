import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    return int(data)


def power(x, y, serial):
    rack = x + 10
    power = rack * y
    power += serial
    power *= rack
    return (power // 100 % 10) - 5


def part_a(data):
    return ",".join(
        map(
            str,
            max(
                [(x, y) for x in range(298) for y in range(298)],
                key=lambda coords: sum(
                    power(x, y, data) for x in range(coords[0], coords[0] + 3) for y in range(coords[1], coords[1] + 3)
                ),
            ),
        )
    )


def part_b(data):
    SIZE = 300
    grid = [[power(x + 1, y + 1, data) for y in range(300)] for x in range(300)]
    summed = defaultdict(int)
    for x in range(300):
        for y in range(300):
            summed[(x, y)] = grid[x][y] + summed[(x - 1, y)] + summed[(x, y - 1)] - summed[(x - 1, y - 1)]

    m = -float("inf")
    mxy = (0, 0, 0)
    for x in range(300):
        for y in range(300):
            for size in range(SIZE - max(x, y)):
                k = summed[(x + size, y + size)] + summed[(x, y)] - summed[(x + size, y)] - summed[(x, y + size)]
                if k > m:
                    m = k
                    mxy = (x, y, size)

    return ",".join(map(str, mxy))


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day11.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 11 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=11, year=2018)

    print("Running day 11 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=11, year=2018)
