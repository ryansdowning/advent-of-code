import time
from copy import deepcopy

from aocd import submit

from pyutils import utils
from pyutils.parsing import recursively_split


def parse(data):
    return recursively_split(data, [(",", None), ("-", lambda x: tuple(map(int, x)))])


def part_a(data):
    total = 0
    for start, end in data:
        for i in range(start, end + 1):
            num = str(i)
            if len(num) % 2 == 1:
                continue
            mid = len(num) // 2
            if num[:mid] == num[mid:]:
                total += i
    return total


def part_b(data):
    total = 0
    for start, end in data:
        for i in range(start, end + 1):
            num = str(i)
            mid = len(num) // 2
            for size in range(1, mid + 1):
                for offset in range(mid):
                    part = num[offset : offset + size]
                    part_count = num.count(part)
                    if part_count >= 2 and size * part_count == len(num):
                        total += i
                        break
                else:
                    continue
                break
    return total


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
