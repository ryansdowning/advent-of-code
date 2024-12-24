import re
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

multiply_pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
do_pattern = r"do\(\)"
dont_pattern = r"don\'t\(\)"


def parse(data):
    return data


def part_a(data):
    data = [(int(a), int(b)) for a, b in re.findall(multiply_pattern, data)]
    return sum(a * b for a, b in data)


def part_b(data):
    enabled = True
    total = 0
    while re.search(multiply_pattern, data):
        if enabled:
            dont_match = re.search(dont_pattern, data)
            sub_data = data[: dont_match.start()] if dont_match else data
            total += part_a(sub_data)
            data = data[dont_match.end() :] if dont_match else ""
        else:
            do_match = re.search(do_pattern, data)
            data = data[do_match.end() :] if do_match else ""
        enabled = not enabled
    return total


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day03.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)
    print(data)

    data_a = deepcopy(data)
    print("Running day 3 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=3, year=2024)
    print("Running day 3 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=3, year=2024)
