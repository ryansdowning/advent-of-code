import heapq
import time
from copy import deepcopy
from typing import TypeVar

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


def get_edges(grid, i, j):
    edges = []
    e_cap = ord(grid[i][j]) + 1
    for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if (
            abs(y) + abs(x) == 1
            and 0 <= i + x < len(grid)
            and 0 <= j + y < len(grid[0])
            and ord(grid[i + x][j + y]) <= e_cap
        ):
            edges.append((i + x, j + y))
    return edges


def get_all_edges(grid, i, j):
    edges = []
    for x, y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if abs(y) + abs(x) == 1 and 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]):
            edges.append((i + x, j + y))
    return edges


def build_graph(grid):
    graph = {}
    start = end = None
    for i, row in enumerate(grid):
        for j, chr in enumerate(row):
            if chr == "S":
                start = (i, j)
                grid[i][j] = "a"
            elif chr == "E":
                end = (i, j)
                grid[i][j] = "z"
            graph[(i, j)] = get_edges(grid, i, j)
    return graph, start, end


def parse(data):
    return list(map(lambda line: list(line), data.split("\n")))


def part_a(data):
    graph, start, end = build_graph(data)
    graph = Graph(graph)
    dist = graph.dijkstra(start)
    print(dist[end])
    return


def part_b(data):
    return


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
