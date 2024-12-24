import time
from copy import deepcopy

from aocd import submit

from pyutils import parsing, utils


def parse(data):
    return parsing.recursively_split(data, [("\n", None), (" ", lambda x: list(map(int, x)))])


def report_is_safe(report) -> bool:
    last = report[0]
    is_increasing = report[0] < report[1]
    for i in report[1:]:
        if i > last and not is_increasing:
            return False
        if i < last and is_increasing:
            return False
        if not 1 <= abs(i - last) <= 3:
            return False
        last = i
    return True


def part_a(data):
    return sum(report_is_safe(report) for report in data)


def gen_dampened_reports(report):
    yield report
    for i in range(len(report)):
        yield report[:i] + report[i + 1 :]


def part_b(data):
    return sum(any(report_is_safe(report_i) for report_i in gen_dampened_reports(report)) for report in data)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day02.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)
    print(data)

    data_a = deepcopy(data)
    print("Running day 2 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=2, year=2024)

    print("Running day 2 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=2, year=2024)
