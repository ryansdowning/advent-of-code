import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    return list(map(int, data.split()))


def part_a(data):
    num_children = data.pop(0)
    num_meta = data.pop(0)
    children_total = sum(part_a(data) for _ in range(num_children))
    meta_total = sum(data[:num_meta])
    del data[:num_meta]
    return meta_total + children_total


def part_b(data):
    num_children = data.pop(0)
    num_meta = data.pop(0)
    vals = [part_b(data) for _ in range(num_children)]

    if num_children == 0:
        total = sum(data[:num_meta])
        del data[:num_meta]
        return total

    children_range = set(range(num_children))
    children_total = sum(vals[i - 1] for i in data[:num_meta] if i - 1 in children_range)
    del data[:num_meta]
    return children_total


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day08.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 8 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=8, year=2018)

    print("Running day 8 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=8, year=2018)
