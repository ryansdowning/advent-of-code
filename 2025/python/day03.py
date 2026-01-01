import time
from copy import deepcopy

from aocd import submit

from pyutils import utils
from pyutils.parsing import recursively_split


def parse(data):
    return list(map(lambda bank: list(map(int, list(bank))), data.split("\n")))


def get_max_bank_joltage(bank: list[int], num_batteries: int) -> int:
    n = len(bank)
    start = 0
    joltage = 0

    for remaining in range(num_batteries, 0, -1):
        end = n - (remaining - 1)
        segment = bank[start:end]
        max_digit = max(segment)
        max_idx = segment.index(max_digit)

        joltage = joltage * 10 + max_digit
        start = start + max_idx + 1

    return joltage


def part_a(data):
    return sum(get_max_bank_joltage(bank, 2) for bank in data)


def part_b(data):
    return sum(get_max_bank_joltage(bank, 12) for bank in data)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day03.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 3 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=3, year=2025)

    print("Running day 3 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=3, year=2025)
