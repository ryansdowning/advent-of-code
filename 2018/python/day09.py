import re
import time
from collections import defaultdict, deque
from copy import deepcopy

from aocd import submit

from pyutils import utils

LINE_RE = re.compile("(\d+) players; last marble is worth (\d+) points")


def parse(data) -> tuple[int, int]:
    return tuple(map(int, LINE_RE.match(data).groups()))


def get_highest_score(players: int, last_marble: int) -> int:
    scores = defaultdict(int)
    circle = deque([0])

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            circle.rotate(7)
            scores[marble % players] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)

    return max(scores.values())


def part_a(data):
    return get_highest_score(*data)


def part_b(data):
    players, last_marble = data
    return get_highest_score(players, last_marble * 100)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day09.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 9 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=9, year=2018)

    print("Running day 9 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=9, year=2018)
