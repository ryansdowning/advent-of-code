import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


# #1 @ 82,901: 26x12
def parse_line(line):
    left, right = line.split(" @ ")
    num1 = int(left[1:])

    left, right = right.split(": ")
    num2, num3 = left.split(",")
    num2, num3 = int(num2), int(num3)

    left, right = right.split("x")
    return num1, num2, num3, int(left), int(right)


def parse(data):
    return list(map(parse_line, data.split("\n")))


def update_fabric(claim, fabric):
    _, x_start, y_start, x_len, y_len = claim
    for x in range(x_start, x_start + x_len):
        for y in range(y_start, y_start + y_len):
            fabric[y][x] += 1


def compute_fabric(data):
    x_size = max(map(lambda x: x[1] + x[3], data))
    y_size = max(map(lambda x: x[2] + x[4], data))

    fabric = [[0 for _ in range(x_size)] for _ in range(y_size)]
    for claim in data:
        update_fabric(claim, fabric)
    return fabric


def part_a(data):
    fabric = compute_fabric(data)
    return sum(i >= 2 for row in fabric for i in row)


def does_claim_overlap(claim, fabric):
    _, x_start, y_start, x_len, y_len = claim
    for x in range(x_start, x_start + x_len):
        for y in range(y_start, y_start + y_len):
            if fabric[y][x] > 1:
                return True
    return False


def part_b(data):
    fabric = compute_fabric(data)
    for claim in data:
        if not does_claim_overlap(claim, fabric):
            return claim[0]


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day03.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 3 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=3, year=2018)

    print("Running day 3 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=3, year=2018)
