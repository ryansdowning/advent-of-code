import itertools
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    lines = data.split("\n")
    out = []
    for line in lines:
        result, numbers = line.split(": ")
        numbers = list(map(int, numbers.split(" ")))
        out.append((int(result), numbers))
    return out


def solve(data, operators):
    total = 0
    for result, numbers in data:
        for operations in itertools.product(operators, repeat=len(numbers) - 1):
            expr_result = numbers[0]
            for operation, number in zip(operations, numbers[1:]):
                if operation == "+":
                    expr_result += number
                elif operation == "*":
                    expr_result *= number
                elif operation == "||":
                    expr_result = int(str(expr_result) + str(number))
            if expr_result == result:
                total += result
                break
    return total


def part_a(data):
    return solve(data, ["+", "*"])


def part_b(data):
    return solve(data, ["+", "*", "||"])


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day07.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 7 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=7, year=2024)

    print("Running day 7 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=7, year=2024)
