import time
from copy import deepcopy
from functools import cmp_to_key

from aocd import submit

from pyutils import parsing, utils


def parse(data):
    return parsing.recursively_split(data, [("\n\n", None), ("\n", lambda x: list(map(eval, x)))])


def is_correct_order(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return False if a > b else True if b > a else None

    if not isinstance(a, list):
        a = [a]
    if not isinstance(b, list):
        b = [b]

    for l, r in zip(a, b):
        recurse = is_correct_order(l, r)
        if recurse is not None:
            return recurse

    return False if len(a) > len(b) else True if len(b) > len(a) else None


def part_a(data):
    return sum(i + 1 for i, (a, b) in enumerate(data) if is_correct_order(a, b))


def part_b(data):
    data = [i for pair in data for i in pair] + [[[2]], [[6]]]
    dividers = [
        i + 1
        for i, packet in enumerate(
            sorted(data, key=cmp_to_key(lambda x, y: is_correct_order(x, y) * 2 - 1), reverse=True)
        )
        if packet == [[2]] or packet == [[6]]
    ]
    return dividers[0] * dividers[1]


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day13.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 13 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=13, year=2022)

    print("Running day 13 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=13, year=2022)
