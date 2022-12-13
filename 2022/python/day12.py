import heapq
import time
from copy import deepcopy
from typing import Callable, TypeVar

from aocd import submit

from pyutils import utils

T = TypeVar("T")


class Graph:
    def __init__(self, graph: dict[T, list[T]]):
        self.graph = graph

    def dijkstra(self, source: T) -> dict[T, int]:
        dist = {k: float("inf") for k in self.graph}
        dist[source] = 0
        seen = set()
        heap = []
        heapq.heappush(heap, (source, dist[source]))

        while len(heap) > 0:
            node, cost = heapq.heappop(heap)
            seen.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in seen:
                    alt = cost + 1
                    if alt < dist[neighbor]:
                        dist[neighbor] = alt
                        heapq.heappush(heap, (neighbor, alt))
        return dist

    def bfs(self, source: T, is_goal: Callable[[T], bool]):
        visited = set()
        queue = {source}
        steps = 1
        while queue:
            queue = set(neighbor for node in queue for neighbor in self.graph[node] if neighbor not in visited)
            visited |= queue
            if any(is_goal(node) for node in queue):
                return steps
            steps += 1
        return float("inf")


def get_neighbors(grid, i, j):
    neighbors = []
    elevation_max = ord(grid[i][j]) + 1
    for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]) and ord(grid[i + x][j + y]) <= elevation_max:
            neighbors.append((i + x, j + y))
    return neighbors


def build_graph(grid):
    graph = {}
    start = end = None
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == "S":
                start = (i, j)
                grid[i][j] = "a"
            elif char == "E":
                end = (i, j)
                grid[i][j] = "z"
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            graph[(i, j)] = get_neighbors(grid, i, j)
    return graph, start, end


def parse(data):
    grid = list(map(lambda line: list(line), data.split("\n")))
    graph, start, end = build_graph(grid)
    return Graph(graph), start, end, grid


def part_a(data):
    graph, start, end, _ = data
    return graph.bfs(start, lambda node: node == end)


def part_b(data):
    graph, _, end, grid = data
    starts = [(x, y) for x, y in graph.graph if grid[x][y] == "a"]
    return min(graph.bfs(coord, lambda node: node == end) for coord in starts)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day12.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 12 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=12, year=2022)

    print("Running day 12 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=12, year=2022)
