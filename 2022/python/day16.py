import re
import time
from collections import defaultdict
from copy import deepcopy
from functools import reduce

from aocd import submit

from pyutils import utils

LINE_RE = re.compile(r"^Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (.*)$")


def parse_groups(groups: tuple[str, str, str]) -> tuple[str, int, list[str]]:
    return groups[0], int(groups[1]), groups[2].split(", ")


def parse(data) -> dict[str, tuple[int, list[str]]]:
    return reduce(
        lambda acc, curr: {curr[0]: curr[1:], **acc},
        map(lambda line: parse_groups(LINE_RE.match(line).groups()), data.split("\n")),
        {},
    )


def get_shortest_path(source: str, target: str, data: dict[str, tuple[int, list[str]]]) -> float:
    queue = [(source, 0)]
    costs = defaultdict(lambda: float("inf"))
    while queue:
        position, cost = queue.pop(0)
        if position == target:
            break

        for neighbor in data[position][1]:
            alt = cost + 1
            if alt < costs[neighbor]:
                costs[neighbor] = alt
                queue.append((neighbor, alt))

    return costs[target]


def get_lowest_costs(valves: list[str]) -> dict[str, dict[str, int]]:
    costs = defaultdict(dict)
    for idx, source in enumerate(valves):
        for target in valves[idx + 1 :]:
            cost = get_shortest_path(source, target, data)
            costs[source][target] = cost
            costs[target][source] = cost

    return costs


def get_possible_paths(
    costs: dict[str, dict[str, int]], data: dict[str, tuple[int, list[str]]], min_remaining: int
) -> dict[frozenset, int]:
    paths = defaultdict(lambda: float("-inf"))
    queue = [("AA", 0, min_remaining, set())]

    while queue:
        valve, total_flow, min_remaining, visited = queue.pop(0)
        neighbors = {
            neighbor for neighbor in costs[valve] if neighbor not in visited and costs[valve][neighbor] < min_remaining
        }
        paths[frozenset(visited)] = max(paths[frozenset(visited)], total_flow)

        for neighbor in neighbors:
            flow = (min_remaining - costs[valve][neighbor] - 1) * data[neighbor][0]
            queue.append(
                (neighbor, total_flow + flow, min_remaining - costs[valve][neighbor] - 1, visited | {neighbor})
            )

    return paths


def release_pressure(data: dict[str, tuple[int, list[str]]], minutes: int) -> dict[frozenset, int]:
    valves = [valve for valve, info in data.items() if info[0] > 0] + ["AA"]
    costs = get_lowest_costs(valves)
    return get_possible_paths(costs, data, minutes)


def part_a(data: dict[str, tuple[int, list[str]]]) -> int:
    paths = release_pressure(data, 30)
    return max(paths.values())


def part_b(data: dict[str, tuple[int, list[str]]]) -> int:
    paths = release_pressure(data, 26)
    return max(flow1 + flow2 for path1, flow1 in paths.items() for path2, flow2 in paths.items() if not path1 & path2)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day16.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 16 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=16, year=2022)

    print("Running day 16 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=16, year=2022)
