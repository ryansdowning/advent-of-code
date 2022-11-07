import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data: str) -> str:
    return data


def react(data: str) -> str:
    reacted = True
    idx = 0
    while reacted:
        for i, (prev_char, curr_char) in enumerate(zip(data[idx:], data[idx + 1 :]), idx):
            if abs(ord(prev_char) - ord(curr_char)) == 32:
                data = data[:i] + data[i + 2 :]
                idx = max(i - 1, 0)
                break
        else:
            reacted = False
    return data


def part_a(data: str) -> int:
    return len(react(data))


def part_b(data: str) -> int:
    unique_letters = set(data.lower())
    reacted_polymers = (react(data.replace(char, "").replace(char.upper(), "")) for char in unique_letters)
    return min(map(len, reacted_polymers))


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day05.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 5 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=5, year=2018)

    print("Running day 5 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=5, year=2018)
