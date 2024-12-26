import itertools
import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils


class Map:
    def __init__(self, data):
        self.columns = data.index("\n")
        data = data.replace("\n", "")
        self.data = data
        self.rows = len(data) // self.columns
        self.antennas = defaultdict(set)
        for i, char in enumerate(data):
            if char == ".":
                continue
            self.antennas[char].add(divmod(i, self.columns))

    def inbounds(self, pos: tuple[int, int]):
        return 0 <= pos[0] < self.rows and 0 <= pos[1] < self.columns


def shift_bool(b: bool):
    # Converts bool to -1, 1.
    return (2 * b) - 1


def step(pos: tuple[int, int], direction: tuple[int, int]):
    return (pos[0] + direction[0], pos[1] + direction[1])


def get_antinodes_for_pair(pair: tuple[tuple[int, int], tuple[int, int]], map: Map):
    a, b = pair
    diff = (abs(b[0] - a[0]), abs(b[1] - a[1]))
    diff_a = (diff[0] * shift_bool(a[0] > b[0]), diff[1] * shift_bool(a[1] > b[1]))
    diff_b = (diff[0] * shift_bool(b[0] > a[0]), diff[1] * shift_bool(b[1] > a[1]))
    antinode_a = step(a, diff_a)
    antinode_b = step(b, diff_b)
    return antinode_a, antinode_b


def get_all_antinodes_for_pair(pair: tuple[tuple[int, int], tuple[int, int]], map: Map):
    a, b = pair
    diff = (abs(b[0] - a[0]), abs(b[1] - a[1]))
    diff_a = (diff[0] * shift_bool(a[0] > b[0]), diff[1] * shift_bool(a[1] > b[1]))
    diff_b = (diff[0] * shift_bool(b[0] > a[0]), diff[1] * shift_bool(b[1] > a[1]))

    antinodes = set()
    curr = step(a, diff_b)  # Step backwards to being so the overlap is counted.
    while map.inbounds(curr):
        antinodes.add(curr)
        curr = step(curr, diff_a)

    curr = step(b, diff_a)
    while map.inbounds(curr):
        antinodes.add(curr)
        curr = step(curr, diff_b)

    return antinodes


def parse(data):
    return Map(data)


def part_a(data: Map):
    antinodes = set()
    for positions in data.antennas.values():
        for pair in itertools.combinations(positions, 2):
            pair_antinodes = get_antinodes_for_pair(pair, data)
            for antinode in pair_antinodes:
                if data.inbounds(antinode):
                    antinodes.add(antinode)
    return len(antinodes)


def part_b(data):
    antinodes = set()
    for positions in data.antennas.values():
        for pair in itertools.combinations(positions, 2):
            pair_antinodes = get_all_antinodes_for_pair(pair, data)
            antinodes.update(pair_antinodes)
    return len(antinodes)


def print_antinodes(map: Map, antinodes: set[tuple[int, int]]):
    data = map.data
    for antinode in antinodes:
        index = antinode[0] * map.columns + antinode[1]
        data = data[:index] + "#" + data[index + 1 :]
    lines = [data[map.columns * i : map.columns * (i + 1)] for i in range(map.rows)]
    print("\n".join(lines))


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day08.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 8 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=8, year=2024)

    print("Running day 8 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=8, year=2024)
