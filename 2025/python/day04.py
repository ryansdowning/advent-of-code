import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

ROLL = "@"


def parse(data: str) -> list[str]:
    return data.split("\n")


def count_adjacent_rolls(data: list[str], x: int, y: int) -> int:
    return (
        sum(
            data[i][j] == ROLL
            for i in range(max(0, x - 1), min(len(data), x + 2))
            for j in range(max(0, y - 1), min(len(data[i]), y + 2))
        )
        - 1
    )  # Subtract 1 to exclude self.


def part_a(data: list[str]) -> int:
    count = sum(
        item == ROLL and count_adjacent_rolls(data, x, y) < 4
        for x, row in enumerate(data)
        for y, item in enumerate(row)
    )
    return count


def part_b(data: list[str]) -> int:
    total = 0
    while True:
        pos_to_remove = [
            (x, y)
            for x, row in enumerate(data)
            for y, item in enumerate(row)
            if item == ROLL and count_adjacent_rolls(data, x, y) < 4
        ]
        if not pos_to_remove:
            break
        for x, y in pos_to_remove:
            data[x] = data[x][:y] + "." + data[x][y + 1 :]
            total += 1
    return total


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day04.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 4 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=4, year=2025)

    print("Running day 4 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=4, year=2025)
