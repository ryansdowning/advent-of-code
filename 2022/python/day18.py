import time
from copy import deepcopy

from aocd import submit

from pyutils import parsing, utils

DIRS = ([1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1])


def parse(data):
    return set(parsing.recursively_split(data, [("\n", None), (",", lambda x: tuple(map(int, x)))]))


def count_sides_covered(data, pos):
    x, y, z = pos
    return sum((x + xd, y + yd, z + zd) in data for xd, yd, zd in DIRS)


def part_a(data):
    return sum(6 - count_sides_covered(data, pos) for pos in data)


def part_b(data):
    visible = 0
    visited = set()
    queue = [(0, 0, 0)]

    while queue:
        x, y, z = queue.pop(0)
        visited.add((x, y, z))
        for xd, yd, zd in DIRS:
            coord = (x + xd, y + yd, z + zd)
            if coord not in visited and coord not in queue and all(-1 <= i <= 22 for i in coord):
                if coord in data:
                    visible += 1
                else:
                    queue.append(coord)
    return visible


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day18.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 18 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=18, year=2022)

    print("Running day 18 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=18, year=2022)
