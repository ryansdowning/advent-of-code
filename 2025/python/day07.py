import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data: str) -> str:
    return data


def part_a(data):
    start_line, *lines = data.split("\n")
    start_pos = start_line.index("S")
    tachyons = {start_pos}
    split_counts = 0
    for line in lines:
        initial_tachyons = deepcopy(tachyons)
        for idx in initial_tachyons:
            if line[idx] == "^":
                split_counts += 1
                tachyons.remove(idx)
                tachyons.add(idx - 1)
                tachyons.add(idx + 1)
    return split_counts


def part_b(data):
    grid = data.split("\n")
    start_col = grid[0].index("S")

    timelines = defaultdict(int)
    timelines[start_col] = 1

    for row in grid[1:]:
        splitters = {i for i, c in enumerate(row) if c == "^"}
        if not splitters:
            continue

        new_timelines = defaultdict(int)
        for col, count in timelines.items():
            if col in splitters:
                new_timelines[col - 1] += count
                new_timelines[col + 1] += count
            else:
                new_timelines[col] += count
        timelines = new_timelines

    return sum(timelines.values())


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day07.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 7 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=7, year=2025)

    print("Running day 7 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=7, year=2025)
