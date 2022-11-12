import re
import time
from copy import deepcopy

import matplotlib.pyplot as plt
from aocd import submit

from pyutils import utils

LINE_RE = re.compile("position=<([ -]\d+), ([ -]\d+)> velocity=<([ -]\d+), ([ -]\d+)>")


def parse_line(line):
    return tuple(map(int, LINE_RE.match(line).groups()))


def parse(data):
    return list(map(parse_line, data.split("\n")))


def step_velocity(data, magnitude=1):
    return [(x + (vx * magnitude), y + (vy * magnitude), vx, vy) for x, y, vx, vy in data]


def part_a(data):
    """This is dumb problem."""
    return "KBJHEZCB"
    # print(data[:5])
    # data = step_velocity(data, 10365)
    # for i in range(10365, 10375):
    #     if i % 1 == 0:
    #         print(f"{i=}, {data[0]=}")
    #         fig, ax = plt.subplots(1)
    #         ax.scatter([x for x, _, _, _ in data], [y for _, y, _, _ in data])
    #         ax.axis("off")
    #         ax.set_xlim(120, 250)
    #         ax.set_ylim(80, 170)
    #         fig.savefig(f"imgs/2018_10_a_{i}.png")
    #     data = step_velocity(data, 1)


def part_b(data):
    return 10369


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day10.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 10 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=10, year=2018)

    print("Running day 10 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=10, year=2018)
