import math
import time
from collections.abc import Sequence
from copy import deepcopy
from typing import LiteralString

from aocd import data, submit

from pyutils import utils


def parse(data: str) -> list[str]:
    return data.split("\n")


def compute(operand: str, values: Sequence[int]) -> int:
    return sum(values) if operand == "+" else math.prod(values)


def part_a(data):
    rows = [line.split() for line in data]
    parsed = [(*tuple(map(int, col[:-1])), col[-1]) for col in zip(*rows)]
    return sum(compute(op, values) for *values, op in parsed)


def part_b(data):
    *value_lines, operand_line = data
    start_indexes = [i for i, c in enumerate(operand_line) if c == "+" or c == "*"]
    end_indexes = start_indexes[1:] + [len(value_lines[0])]
    operands = [operand_line[i] for i in start_indexes]

    total = 0
    for start, end, op in zip(start_indexes, end_indexes, operands):
        values = []
        for col in range(end - 1, start - 1, -1):
            digits = "".join(line[col] for line in value_lines).replace(" ", "")
            if digits:
                values.append(int(digits))
        total += compute(op, values)
    return total


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day06.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 6 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=6, year=2025)

    print("Running day 6 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=6, year=2025)
