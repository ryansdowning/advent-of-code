import time
from copy import deepcopy

from aocd import submit

from pyutils import utils
from pyutils.parsing import recursively_split


def parse(data):
    return recursively_split(data, [("\n", None), (" ", lambda x: (x[0], int(x[1])))])


DIR_MAP = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}


def update_tail(h, t):
    xd, yd = h[0] - t[0], h[1] - t[1]
    x = y = 0
    if xd > 1:
        x += 1
        if yd > 0:
            y += 1
        elif yd < 0:
            y -= 1
    elif xd < -1:
        x -= 1
        if yd > 0:
            y += 1
        elif yd < 0:
            y -= 1
    elif yd > 1:
        y += 1
        if xd > 0:
            x += 1
        elif xd < 0:
            x -= 1
    elif yd < -1:
        y -= 1
        if xd > 0:
            x += 1
        elif xd < 0:
            x -= 1
    return (t[0] + x, t[1] + y)


def part_a(data):
    h = (0, 0)
    t = (0, 0)
    ts = {t}

    for direction, steps in data:
        xd, yd = DIR_MAP[direction]
        for _ in range(steps):
            h = (h[0] + xd, h[1] + yd)
            t = update_tail(h, t)
            ts.add(t)
    return len(ts)


def part_b(data):
    knots = [(0, 0)] * 10
    ts = {(0, 0)}

    for direction, steps in data:
        xd, yd = DIR_MAP[direction]
        for _ in range(steps):
            knots[0] = (knots[0][0] + xd, knots[0][1] + yd)
            for prev, curr in zip(range(10), range(1, 10)):
                knots[curr] = update_tail(knots[prev], knots[curr])
            ts.add(knots[-1])
    return len(ts)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day09.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 9 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=9, year=2022)

    print("Running day 9 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=9, year=2022)
