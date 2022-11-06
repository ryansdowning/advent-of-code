import datetime
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse_line(data):
    date, msg = data.split(" ")
    return datetime.strptime(date, "[%Y-%m-%d] %H:%M"), msg


def parse(data):
    return list(map(parse_line, data.split("\n")))


def part_a(data):
    return


def part_b(data):
    return


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day04.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 4 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=4, year=2018)

    print("Running day 4 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=4, year=2018)
