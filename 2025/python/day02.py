import bisect
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils
from pyutils.parsing import recursively_split


def parse(data):
    return recursively_split(data, [(",", None), ("-", lambda x: tuple(map(int, x)))])


def sum_in_ranges(candidates, data):
    """Sum all candidates that fall within any range in data."""
    ranges = sorted(data)
    starts = [s for s, _ in ranges]

    total = 0
    for num in candidates:
        idx = bisect.bisect_right(starts, num) - 1
        if idx >= 0 and ranges[idx][0] <= num <= ranges[idx][1]:
            total += num
    return total


def generate_doubled_ids(max_val):
    """Generate all numbers that are a pattern repeated exactly twice."""
    invalid = set()
    max_digits = len(str(max_val))

    for pattern_len in range(1, max_digits // 2 + 1):
        start = 10 ** (pattern_len - 1)
        for pattern in range(start, 10**pattern_len):
            num = int(str(pattern) * 2)
            if num <= max_val:
                invalid.add(num)
    return invalid


def part_a(data):
    max_val = max(end for _, end in data)
    return sum_in_ranges(generate_doubled_ids(max_val), data)


def generate_invalid_ids(max_val):
    """Generate all numbers that are a pattern repeated 2+ times, up to max_val."""
    invalid = set()
    max_digits = len(str(max_val))

    for pattern_len in range(1, max_digits // 2 + 1):
        start = 10 ** (pattern_len - 1)
        end = 10**pattern_len

        for pattern in range(start, end):
            pattern_str = str(pattern)
            for repeats in range(2, max_digits // pattern_len + 1):
                num = int(pattern_str * repeats)
                if num > max_val:
                    break
                invalid.add(num)

    return invalid


def part_b(data):
    max_val = max(end for _, end in data)
    return sum_in_ranges(generate_invalid_ids(max_val), data)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day02.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 2 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=2, year=2025)

    print("Running day 2 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=2, year=2025)
