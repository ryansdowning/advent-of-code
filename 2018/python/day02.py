import time
from collections import Counter
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    return data.split("\n")


def part_a(data):
    counts = list(map(lambda x: set(x.values()), map(Counter, data)))
    twos = sum(2 in count for count in counts)
    threes = sum(3 in count for count in counts)
    return twos * threes


def is_diff_by_1(a, b):
    flag = False
    for i, j in zip(a, b):
        if i != j:
            if flag:
                return False
            flag = True
    return flag


def part_b(data):
    for i, a in enumerate(data, 1):
        for b in data[i:]:
            if is_diff_by_1(a, b):
                return "".join(letter for letter, other in zip(a, b) if letter == other)
    return ""


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day02.txt", "r") as fp:
        data = fp.read()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 2 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=2, year=2018)

    print("Running day 2 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=2, year=2018)
