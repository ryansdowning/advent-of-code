import re
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

MOVE_RE = re.compile("move (\d+) from (\d+) to (\d+)")


def parse_start(start: str) -> list[list[str]]:
    rows = [
        [line[i : i + 3][1] if line[i : i + 3] != "   " else None for i in range(0, len(line), 4)]
        for line in start.split("\n")[:-1]
    ]
    columns = list(zip(*rows))
    columns = [[i for i in col if i is not None] for col in columns]
    return columns


def process_move(
    stacks: list[list[str]], quantity: int, stack1: int, stack2: int, *, is_part_b: bool = False
) -> list[list[str]]:
    blocks = stacks[stack1 - 1][:quantity]
    if not is_part_b:
        blocks = blocks[::-1]

    stacks[stack1 - 1] = stacks[stack1 - 1][quantity:]
    stacks[stack2 - 1] = blocks + stacks[stack2 - 1]
    return stacks


def parse(data: str) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    start, moves = data.split("\n\n")
    stacks = parse_start(start)
    moves = [tuple(map(int, MOVE_RE.match(move).groups())) for move in moves.split("\n")]
    return stacks, moves


def part_a(data: tuple):
    stacks, moves = data
    for move in moves:
        stacks = process_move(stacks, *move)

    return "".join(stack[0] for stack in stacks)


def part_b(data):
    stacks, moves = data
    for move in moves:
        stacks = process_move(stacks, *move, is_part_b=True)

    return "".join(stack[0] for stack in stacks)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day05.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 5 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=5, year=2022)

    print("Running day 5 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=5, year=2022)
