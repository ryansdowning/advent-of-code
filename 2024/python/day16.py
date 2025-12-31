import heapq
import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


class Map:
    def __init__(self, data: str):
        self.columns = data.index("\n")
        data = data.replace("\n", "")
        self.data = data
        self.rows = len(data) // self.columns

        self.walls = set()
        self.start = None
        self.end = None
        for i, char in enumerate(data):
            if char == "#":
                self.walls.add(divmod(i, self.columns))
            elif char == "S":
                self.start = divmod(i, self.columns)
            elif char == "E":
                self.end = divmod(i, self.columns)

    def is_wall(self, pos: tuple[int, int]) -> bool:
        return pos in self.walls

    def get_minimum_cost(self) -> int:
        """Modified Dijkstra's algorithm to find the minimum cost to reach the end"""
        queue = []
        heapq.heappush(queue, (0, self.start, (0, 1)))
        min_cost = {}

        while queue:
            cost, current, direction = heapq.heappop(queue)
            if cost >= min_cost.get((current, direction), float("inf")):
                continue
            min_cost[(current, direction)] = cost

            if current == self.end:
                return cost

            for new_direction in DIRECTIONS:
                new_pos = (current[0] + new_direction[0], current[1] + new_direction[1])

                if self.is_wall(new_pos):
                    continue

                move_cost = 1 + (new_direction != direction) * 1000
                new_cost = cost + move_cost
                heapq.heappush(queue, (new_cost, new_pos, new_direction))

        return float("inf")

    def get_minimum_cost_paths(self) -> list[list[tuple[int, int]]]:
        queue = []
        heapq.heappush(queue, (0, self.start, (0, 1), [self.start]))
        min_cost = {}
        paths = defaultdict(list)

        while queue:
            cost, current, direction, path = heapq.heappop(queue)

            if cost > min_cost.get((current, direction), float("inf")):
                continue

            if cost < min_cost.get((current, direction), float("inf")):
                min_cost[(current, direction)] = cost
                paths[current] = [path]
            elif cost == min_cost.get((current, direction), float("inf")):
                paths[current].append(path)

            if current == self.end:
                continue

            for new_direction in DIRECTIONS:
                new_pos = (current[0] + new_direction[0], current[1] + new_direction[1])

                if self.is_wall(new_pos):
                    continue

                move_cost = 1 + (new_direction != direction) * 1000
                new_cost = cost + move_cost
                heapq.heappush(queue, (new_cost, new_pos, new_direction, path + [new_pos]))

        return paths[self.end] if self.end in paths else []


def parse(data):
    #     data = """###############
    # #.......#....E#
    # #.#.###.#.###.#
    # #.....#.#...#.#
    # #.###.#####.#.#
    # #.#.#.......#.#
    # #.#.#####.###.#
    # #...........#.#
    # ###.#.#####.#.#
    # #...#.....#.#.#
    # #.#.#.###.#.#.#
    # #.....#...#.#.#
    # #.###.#.#.#.#.#
    # #S..#.....#...#
    # ###############"""
    #     data = """#################
    # #...#...#...#..E#
    # #.#.#.#.#.#.#.#.#
    # #.#.#.#...#...#.#
    # #.#.#.#.###.#.#.#
    # #...#.#.#.....#.#
    # #.#.#.#.#.#####.#
    # #.#...#.#.#.....#
    # #.#.#####.#.###.#
    # #.#.#.......#...#
    # #.#.###.#####.###
    # #.#.#...#.....#.#
    # #.#.#.#####.###.#
    # #.#.#.........#.#
    # #.#.#.#########.#
    # #S#.............#
    # #################"""
    return Map(data)


def part_a(data: Map):
    return data.get_minimum_cost()


def part_b(data: Map):
    paths = data.get_minimum_cost_paths()
    return len(set(pos for path in paths for pos in path))


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day16.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 16 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    # submit(solution_a, part="a", day=16, year=2024)

    print("Running day 16 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    # submit(solution_b, part="b", day=16, year=2024)
