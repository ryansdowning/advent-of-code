import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

ABC_MAP = {"A": 1, "B": 2, "C": 3}
XYZ_MAP = {"X": 1, "Y": 2, "Z": 3}
WINS_MAP = {1: 2, 2: 3, 3: 1}
LOSES_MAP = {1: 3, 2: 1, 3: 2}


def score(round):
    if round[0] == round[1]:
        return round[1] + 3
    if WINS_MAP[round[0]] == round[1]:
        return 6 + round[1]
    return round[1]


def parse_round(round):
    return (ABC_MAP[round[0]], XYZ_MAP[round[1]])


def parse(data):
    return [parse_round(round.split(" ")) for round in data.split("\n")]


def part_a(data):
    return sum(map(score, data))


def score_b(round):
    if round[1] == 1:
        return LOSES_MAP[round[0]]
    if round[1] == 2:
        return 3 + round[0]
    return 6 + WINS_MAP[round[0]]


def part_b(data):
    return sum(map(score_b, data))


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day02.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 2 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=2, year=2022)

    print("Running day 2 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=2, year=2022)
