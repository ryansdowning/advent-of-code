import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    return data.split("\n")


def get_prio(char):
    prio = ord(char)
    if prio >= 97:
        return prio - 96
    return prio - 38


def part_a(data):
    total = 0
    for sack in data:
        size = len(sack)
        l, r = set(sack[: size // 2]), set(sack[size // 2 :])
        prio = (l & r).pop()
        total += get_prio(prio)

    return total


def part_b(data):
    total = 0
    for idx in range(0, len(data), 3):
        a, b, c = data[idx : idx + 3]
        prio = set(a) & set(b) & set(c)
        prio = prio.pop()
        total += get_prio(prio)

    return total


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day03.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 3 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=3, year=2022)

    print("Running day 3 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=3, year=2022)
