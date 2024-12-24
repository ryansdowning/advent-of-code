import time
from collections import Counter
from copy import deepcopy

from aocd import submit

from pyutils import parsing, utils


def parse(data):
    items = parsing.recursively_split(data, [("\n", None), ("   ", lambda x: list(map(int, x)))])
    return list(zip(*items))


def part_a(data):
    a, b = data
    sorted_a = sorted(a)
    sorted_b = sorted(b)
    return sum(abs(i - j) for i, j in zip(sorted_a, sorted_b))


def part_b(data):
    counter = Counter(data[1])
    return sum(i * counter[i] for i in data[0])


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day01.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 1 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=1, year=2024)

    print("Running day 1 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=1, year=2024)
