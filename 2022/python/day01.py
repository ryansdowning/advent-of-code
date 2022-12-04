import time
from copy import deepcopy

import matplotlib.pyplot as plt
from aocd import submit

from pyutils import parsing, utils


def parse(data):
    items = parsing.recursively_split(data, [("\n\n", None), ("\n", lambda x: list(map(int, x)))])
    totals = [sum(cals) for cals in items]
    return totals


def part_a(data):
    # Visualization.
    # max_idx = max(range(len(data)), key=lambda idx: data[idx])
    # colors = ["#1f77b4"] * len(data)
    # colors[max_idx] = "r"
    # fig, ax = plt.subplots(1, figsize=(15, 6))
    # ax.bar(range(len(data)), data, color=colors)
    # rect = ax.patches[max_idx]
    # height = rect.get_height()
    # ax.text(
    #     rect.get_x() + rect.get_width() / 2, height + 5, data[max_idx], ha="center", va="bottom"
    # )
    # ax.set_xlabel("Elf ID")
    # ax.set_ylabel("Calories")
    # fig.savefig("viz/2022/2022-01-a.png")
    # End Visualization.
    return max(data)


def part_b(data):
    idxs = sorted(range(len(data)), key=lambda idx: data[idx])
    top = idxs[-3:]
    cals = sum(data[idx] for idx in top)

    # Visualization.
    # colors = ["#1f77b4"] * len(data)
    # fig, ax = plt.subplots(1, figsize=(15, 6))
    # ax.set_xlabel("Elf ID")
    # ax.set_ylabel("Calories")
    # for idx in top:
    #     colors[idx] = "r"

    # ax.bar(range(len(data)), data, color=colors)
    # rects = ax.patches
    # for idx in top:
    #     rect = rects[idx]
    #     height = rect.get_height()
    #     ax.text(
    #         rect.get_x() + rect.get_width() / 2, height + 5, data[idx], ha="center", va="bottom"
    #     )

    # fig.savefig("viz/2022/2022-01-b.png")
    # End visualization.

    return cals


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day01.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 1 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=1, year=2022)

    print("Running day 1 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=1, year=2022)
