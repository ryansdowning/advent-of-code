import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils

DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


class Map:
    def __init__(self, data):
        self.columns = data.index("\n")
        self.grid = [list(map(int, line)) for line in data.splitlines()]
        self.rows = len(self.grid[0])

    def is_inbounds(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self.rows and 0 <= pos[1] < self.columns

    def find_roots(self, pos: tuple[int, int]) -> set[tuple[int, int]]:
        val = self.grid[pos[0]][pos[1]]
        if val == 0:
            return {pos}

        roots = set()
        for direction in DIRECTIONS:
            new = (pos[0] + direction[0], pos[1] + direction[1])
            if self.is_inbounds(new) and self.grid[new[0]][new[1]] == val - 1:
                roots = roots.union(self.find_roots(new))
        return roots

    def find_num_paths_to_peak(self, pos: tuple[int, int], num_paths=0) -> set[tuple[int, int]]:
        val = self.grid[pos[0]][pos[1]]
        if val == 9:
            return num_paths + 1

        total = 0
        for direction in DIRECTIONS:
            new = (pos[0] + direction[0], pos[1] + direction[1])
            if self.is_inbounds(new) and self.grid[new[0]][new[1]] == val + 1:
                total += self.find_num_paths_to_peak(new, num_paths)
        return total


def parse(data):
    return Map(data)


def part_a(data: Map):
    peaks = set()
    for i, row in enumerate(data.grid):
        for j, val in enumerate(row):
            if val == 9:
                peaks.add((i, j))

    peak_roots = {peak: data.find_roots(peak) for peak in peaks}
    root_peaks = defaultdict(set)
    for peak, roots in peak_roots.items():
        for root in roots:
            root_peaks[root].add(peak)
    return sum(len(peaks) for peaks in root_peaks.values())


def part_b(data: Map):
    trailheads = set()
    for i, row in enumerate(data.grid):
        for j, val in enumerate(row):
            if val == 0:
                trailheads.add((i, j))

    trailhead_paths = {trailhead: data.find_num_paths_to_peak(trailhead) for trailhead in trailheads}
    return sum(num_paths for num_paths in trailhead_paths.values())


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day10.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 10 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=10, year=2024)

    print("Running day 10 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=10, year=2024)
