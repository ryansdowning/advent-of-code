import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils

VERTICAL_DIRS = [(1, 0), (-1, 0)]
HORIZONTAL_DIRS = [(0, 1), (0, -1)]
DIRECTIONS = [*VERTICAL_DIRS, *HORIZONTAL_DIRS]


class Map:
    def __init__(self, data: str):
        self.columns = data.index("\n")
        self.grid = data.splitlines()
        self.rows = len(self.grid[0])

    def is_inbounds(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self.rows and 0 <= pos[1] < self.columns


def parse(data):
    data = Map(data)
    visited = set()
    regions = defaultdict(list)

    def dfs(pos: tuple[int, int], region: str, region_index: int):
        x, y = pos
        if pos in visited or not data.is_inbounds(pos) or data.grid[x][y] != region:
            return

        regions[region][region_index].append(pos)
        visited.add(pos)

        for (dx, dy) in DIRECTIONS:
            dfs((x + dx, y + dy), region, region_index)

    for i, row in enumerate(data.grid):
        for j, val in enumerate(row):
            if (i, j) in visited:
                continue

            curr = (i, j)
            regions[val].append([])
            dfs(curr, val, len(regions[val]) - 1)

    return regions


def get_fence_price(region: list[tuple[int, int]]) -> int:
    region = set(region)
    area = len(region)
    perimeter = sum((x + dx, y + dy) not in region for x, y in region for dx, dy in DIRECTIONS)
    return area * perimeter


def part_a(regions: dict[str, list[list[tuple[int, int]]]]):
    return sum(get_fence_price(region) for letter_regions in regions.values() for region in letter_regions)


def get_num_region_sides(region: list[tuple[int, int]]) -> int:
    region = set(region)
    perimeter_edges = defaultdict(lambda: defaultdict(list))

    def update_perimeter(direction, pos, a, b):
        if pos not in region:
            perimeter_edges[direction][a].append(b)

    for x, y in region:
        for dx, dy in VERTICAL_DIRS:
            new_pos = (x + dx, y + dy)
            update_perimeter((dx, dy), new_pos, x, y)
        for dx, dy in HORIZONTAL_DIRS:
            new_pos = (x + dx, y + dy)
            update_perimeter((dx, dy), new_pos, y, x)

    sides = 0
    for directional_edges in perimeter_edges.values():
        for edges in directional_edges.values():
            edges = sorted(edges)
            sides += 1 + sum(curr != prev + 1 for prev, curr in zip(edges, edges[1:]))
    return sides


def get_discounted_fence_price(region: list[tuple[int, int]]) -> int:
    region = set(region)
    area = len(region)
    sides = get_num_region_sides(region)
    return area * sides


def part_b(regions: dict[str, list[list[tuple[int, int]]]]) -> int:
    return sum(get_discounted_fence_price(region) for letter_regions in regions.values() for region in letter_regions)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day12.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 12 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=12, year=2024)

    print("Running day 12 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=12, year=2024)
