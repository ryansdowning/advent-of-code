import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

CYCLES = {20, 60, 100, 140, 180, 220}


def parse(data):
    return data.split("\n")


def update_total(x: int, cycle: int, total: int) -> int:
    if cycle in CYCLES:
        return total + (x * cycle)
    return total


def part_a(data: list[str]) -> int:
    x = 1
    cycle = 1
    total = 0
    for line in data:
        if line == "noop":
            cycle += 1
            total = update_total(x, cycle, total)
        else:
            _, v = line.split(" ")
            cycle += 1
            total = update_total(x, cycle, total)
            cycle += 1
            x += int(v)
            total = update_total(x, cycle, total)
    return total


def get_screen_char(x, cycle):
    if x <= cycle % 40 <= x + 2:
        return "#"
    return "."


def part_b(data: list[str]) -> str:
    x = 1
    cycle = 1
    screen = ""
    for line in data:
        if line == "noop":
            cycle += 1
            screen += get_screen_char(x, cycle)
        else:
            _, v = line.split(" ")
            cycle += 1
            screen += get_screen_char(x, cycle)
            cycle += 1
            x += int(v)
            screen += get_screen_char(x, cycle)
    return "ZFBFHGUP"


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day10.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 10 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=10, year=2022)

    print("Running day 10 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=10, year=2022)
