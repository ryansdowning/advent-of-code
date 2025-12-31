import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

INITIAL_POSITION = 50


def parse(data):
    return list(map(lambda x: ((x[0] == "R") * 2 - 1) * int(x[1:]), data.split("\n")))


def part_a(data):
    position = INITIAL_POSITION
    zero_counts = 0
    for move in data:
        position = (position + move) % 100
        zero_counts += position == 0
    return zero_counts


def part_b(data):
    position = INITIAL_POSITION
    zero_counts = 0
    for move in data:
        if move > 0:
            zero_counts += (position + move) // 100
        elif move < 0:
            abs_move = -move
            if position == 0:
                zero_counts += abs_move // 100
            elif abs_move >= position:
                zero_counts += 1 + (abs_move - position) // 100
        position = (position + move) % 100
    return zero_counts


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day01.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 1 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=1, year=2025)

    print("Running day 1 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=1, year=2025)
