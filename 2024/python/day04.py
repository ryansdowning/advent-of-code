import time
from copy import deepcopy

from aocd import submit

from pyutils import parsing, utils

LETTERS = ["X", "M", "A", "S"]
DIAGONAL_STEPS = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
STEPS = [(0, 1), (1, 0), (0, -1), (-1, 0), *DIAGONAL_STEPS]
MS_SET = set(["M", "S"])


def parse(data):
    return parsing.recursively_split(data, [("\n", None)])


def step_is_in_bounds(data, i, j, step):
    return 0 <= i + step[0] < len(data) and 0 <= j + step[1] < len(data[i + step[0]])


def cell_matches_letters(data, i, j, letters=None, step=None):
    if letters is None:
        letters = LETTERS.copy()

    letter = letters.pop()
    if data[i][j] != letter:
        return False
    if len(letters) == 0:
        return True

    if step is None:
        return sum(
            step_is_in_bounds(data, i, j, step)
            and cell_matches_letters(data, i + step[0], j + step[1], letters.copy(), step)
            for step in STEPS
        )
    return step_is_in_bounds(data, i, j, step) and cell_matches_letters(
        data, i + step[0], j + step[1], letters.copy(), step
    )


def part_a(data):
    return sum(cell_matches_letters(data, i, j) for i in range(len(data)) for j in range(len(data[i])))


def forms_x_mas(data, i, j):
    if data[i][j] != "A":
        return False

    if not all(step_is_in_bounds(data, i, j, step) for step in DIAGONAL_STEPS):
        return False

    return (
        data[i + 1][j + 1] in MS_SET
        and data[i - 1][j - 1] in MS_SET
        and data[i + 1][j + 1] != data[i - 1][j - 1]
        and data[i + 1][j - 1] in MS_SET
        and data[i - 1][j + 1] in MS_SET
        and data[i + 1][j - 1] != data[i - 1][j + 1]
    )


def part_b(data):
    return sum(forms_x_mas(data, i, j) for i in range(len(data)) for j in range(len(data[i])))


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day04.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 4 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=4, year=2024)
    print("Running day 4 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=4, year=2024)
