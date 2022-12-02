import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    elves = data.split("\n\n")
    items = [list(map(int, elf.split("\n"))) for elf in elves]
    totals = [sum(cals) for cals in items]
    return totals


def part_a(data):
    return max(data)


def part_b(data):
    cals = 0
    for _ in range(3):
        max_idx = max(range(len(data)), key=lambda idx: data[idx])
        cals += data[max_idx]
        data.pop(max_idx)
    return cals


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day01.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 1 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=1, year=2022)

    print("Running day 1 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=1, year=2022)
