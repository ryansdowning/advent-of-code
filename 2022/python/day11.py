import re
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

MONKEY_RE = re.compile(
    "^Monkey (\d+):\n  Starting items: ([\d\, ]+)\n  Operation: new = ([old\d\*\+ ]+)\n  Test: divisible by (\d+)\n    If true: throw to monkey (\d+)\n    If false: throw to monkey (\d+)$"
)


def parse_operation(operation: str):
    operation = operation[4:]
    operator = operation[0]
    operand = operation[2:]
    if operand.isnumeric():
        operand = int(operand)
    return operator, operand


def clean_values(values):
    monkey_id = int(values[0])
    items = list(map(int, values[1].split(", ")))
    operation = parse_operation(values[2])
    divisible_by = int(values[3])
    if_true = int(values[4])
    if_false = int(values[5])
    return [monkey_id, items, operation, divisible_by, if_true, if_false]


def parse(data):
    return list(map(lambda x: clean_values(MONKEY_RE.match(x).groups()), data.split("\n\n")))


def perform_operation(old, operation, is_part_b):
    operator, operand = operation
    if operand == "old":
        operand = old
    new = old * operand if operator == "*" else old + operand
    return new if is_part_b else new // 3


def get_monkey_bussiness(data, rounds, is_part_b):
    inspections = [0] * len(data)
    mod = 1
    for _, _, _, divisible_by, _, _ in data:
        mod *= divisible_by

    for _ in range(rounds):
        for i in range(len(data)):
            monkey, items, operation, divisible_by, if_true, if_false = data[i]
            for item in items[::]:
                new = perform_operation(item, operation, is_part_b) % mod
                if new % divisible_by == 0:
                    data[if_true][1].append(new)
                else:
                    data[if_false][1].append(new)
            inspections[monkey] += len(items)
            data[i][1] = []

    inspections = sorted(inspections)
    return inspections[-1] * inspections[-2]


def part_a(data):
    return get_monkey_bussiness(data, 20, False)


def part_b(data):
    return get_monkey_bussiness(data, 10000, True)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day11.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 11 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=11, year=2022)

    print("Running day 11 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=11, year=2022)
