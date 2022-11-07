import re
import time
from collections import Counter
from copy import deepcopy

from aocd import submit

from pyutils import utils
from pyutils.algs import distance

# import matplotlib.pyplot as plt

LINE_RE = re.compile("(\d+), (\d+)")


def parse_line(line: str) -> tuple[int, int]:
    return tuple(map(int, LINE_RE.match(line).groups()))


def parse(data: str) -> list[tuple[int, int]]:
    return list(map(parse_line, data.split("\n")))


def part_a(data: list[tuple[int, int]]):
    max_x = max(data, key=lambda x: x[0])[0] + 1
    max_y = max(data, key=lambda x: x[1])[1] + 1

    def get_closest_idx(x, y):
        dists = [distance.manhattan(point, (x, y)) for point in data]
        min_dist_idx = min(range(len(dists)), key=dists.__getitem__)
        min_value = dists.pop(min_dist_idx)
        second_min_value = min(dists)
        return min_dist_idx if min_value != second_min_value else -1

    table = [[get_closest_idx(x, y) for x in range(max_x)] for y in range(max_y)]
    infinite_chars = {
        table[y][x]
        for x, y in [(0, y_) for y_ in range(max_y)]
        + [(max_x - 1, y_) for y_ in range(max_y)]
        + [(x_, 0) for x_ in range(max_x)]
        + [(x_, max_y - 1) for x_ in range(max_x)]
    }
    ignore_chars = infinite_chars | {"."}
    flat_table = [i for row in table for i in row if i not in ignore_chars]
    areas = Counter(flat_table)

    # plt.pcolormesh(table)
    # plt.axis("off")
    # plt.savefig("2018_06_a.png")

    return max(areas.values())


def part_b(data):
    max_dist = 10000
    max_x = max(data, key=lambda x: x[0])[0] + 1
    max_y = max(data, key=lambda x: x[1])[1] + 1

    def get_total_dist(x, y):
        return sum(distance.manhattan(point, (x, y)) for point in data)

    flat_table = (get_total_dist(x, y) < max_dist for x in range(max_x) for y in range(max_y))
    # table = [[get_total_dist(x, y) <  max_dist for x in range(max_x)] for y in range(max_y)]
    # plt.pcolormesh(table)
    # plt.axis("off")
    # plt.savefig("2018_06_b.png")
    # flat_table = [i for row in table for i in row]
    return sum(flat_table)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day06.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 6 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=6, year=2018)

    print("Running day 6 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=6, year=2018)
