import re
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

pattern = re.compile(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)")


def token_cost(a, b):
    return 3 * a + b


def solve_diophantine(eqn1: tuple[int, int, int], eqn2: tuple[int, int, int]) -> tuple[int, int]:
    a1, b1, c1 = eqn1
    a2, b2, c2 = eqn2

    det = a1 * b2 - a2 * b1
    det_x = c1 * b2 - c2 * b1
    x = det_x / det
    if not x.is_integer():
        return None

    det_y = a1 * c2 - a2 * c1
    y = det_y / det
    if not y.is_integer():
        return None

    return int(x), int(y)


def parse(data):
    matches = re.findall(pattern, data)
    return [list(map(int, match)) for match in matches]


def part_a(data):
    total = 0
    for row in data:
        eqn1 = row[0], row[2], row[4]
        eqn2 = row[1], row[3], row[5]
        result = solve_diophantine(eqn1, eqn2)
        if result:
            a, b = result
            total += token_cost(a, b)

    return total


def part_b(data):
    total = 0
    for row in data:
        eqn1 = row[0], row[2], row[4] + 10000000000000
        eqn2 = row[1], row[3], row[5] + 10000000000000
        result = solve_diophantine(eqn1, eqn2)
        if result:
            a, b = result
            total += token_cost(a, b)

    return total


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day13.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 13 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=13, year=2024)

    print("Running day 13 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=13, year=2024)
