import re
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

PATTERN = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")
GRID_SIZE = (101, 103)
QUANDRANTS = [
    ((0, GRID_SIZE[0] // 2 - 1), (0, GRID_SIZE[1] // 2 - 1)),
    ((GRID_SIZE[0] // 2 + 1, GRID_SIZE[0] - 1), (0, GRID_SIZE[1] // 2 - 1)),
    ((0, GRID_SIZE[0] // 2 - 1), (GRID_SIZE[1] // 2 + 1, GRID_SIZE[1] - 1)),
    ((GRID_SIZE[0] // 2 + 1, GRID_SIZE[0] - 1), (GRID_SIZE[1] // 2 + 1, GRID_SIZE[1] - 1)),
]
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]


class Robot:
    def __init__(self, pos: tuple[int, int], vel: tuple[int, int]):
        self.pos = pos
        self.vel = vel

    def update(self, steps=1):
        self.pos = (
            (self.pos[0] + (self.vel[0] * steps)) % GRID_SIZE[0],
            (self.pos[1] + (self.vel[1] * steps)) % GRID_SIZE[1],
        )

    def __str__(self):
        return f"Robot(pos={self.pos}, vel={self.vel})"

    def __repr__(self):
        return str(self)


def parse(data):
    data = [list(map(int, match)) for match in re.findall(PATTERN, data)]
    return [Robot((x, y), (dx, dy)) for x, y, dx, dy in data]


def get_safety_score(robots: list[Robot]) -> int:
    quandrant_counts = [0, 0, 0, 0]
    for robot in robots:
        x, y = robot.pos
        for i, ((min_x, max_x), (min_y, max_y)) in enumerate(QUANDRANTS):
            if min_x <= x <= max_x and min_y <= y <= max_y:
                quandrant_counts[i] += 1
                break

    a, b, c, d = quandrant_counts
    return a * b * c * d


def part_a(data):
    for robot in data:
        robot.update(100)

    return get_safety_score(data)


def get_percent_overlap(positions: set[tuple[int, int]], num_robots: int) -> float:
    return 1 - len(positions) / num_robots


def get_percent_with_neighbors(positions: set[tuple[int, int]]) -> float:
    neighbors = sum(any((x + dx, y + dy) in positions for dx, dy in DIRECTIONS) for x, y in positions)
    return neighbors / len(positions)


def print_robots(robots: list[Robot]):
    grid = [["." for _ in range(GRID_SIZE[1])] for _ in range(GRID_SIZE[0])]
    for robot in robots:
        x, y = robot.pos
        grid[x][y] = "#"

    print("\n".join("".join(row) for row in grid))


def part_b(data):
    i = 0
    num_robots = len(data)
    while True:
        i += 1
        for robot in data:
            robot.update()

        positions = set((robot.pos for robot in data))
        if get_percent_overlap(positions, num_robots) < 0.02 and get_percent_with_neighbors(positions) > 0.5:
            break

    return i


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day14.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)
    print(data)

    data_a = deepcopy(data)
    print("Running day 14 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=14, year=2024)

    print("Running day 14 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=14, year=2024)
