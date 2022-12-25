import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


class Num:
    def __init__(self, value):
        self.value = int(value)


def parse(data):
    return list(map(Num, data.split("\n")))


def part_a(data):
    return mix(data)


def mix(data, rounds=1):
    nums = data.copy()
    for _ in range(rounds):
        for num in data:
            i = nums.index(num)
            new_i = (i + num.value) % (len(nums) - 1)

            nums.insert(new_i, nums.pop(i))

    idx0 = next(i for i, num in enumerate(nums) if num.value == 0)
    return sum(nums[(idx0 + i) % len(data)].value for i in (1000, 2000, 3000))


def part_b(data):
    data = [Num(num.value * 811589153) for num in data]
    return mix(data, 10)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day20.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 20 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=20, year=2022)

    print("Running day 20 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=20, year=2022)
