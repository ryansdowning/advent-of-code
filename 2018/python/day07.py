import re
import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

LINE_RE = re.compile("Step ([A-Z]) must be finished before step ([A-Z]) can begin.")


def solve_dependency_order(dependency_graph):
    """
    Variation of pyutils.graph.solve_dependency_order which only pops one unconstrained dependency (the min) per step.
    """
    dependency_graph = deepcopy(dependency_graph)
    dependencies = set(dependency_graph.keys())
    dependency_order = []

    while dependencies:
        has_no_remaining_dep = set(filter(lambda dep: not dependency_graph[dep], dependencies))
        if not has_no_remaining_dep:
            raise ValueError

        requirement = min(has_no_remaining_dep)
        dependency_order.append(requirement)
        dependencies.remove(requirement)
        for req in dependency_graph:
            dependency_graph[req].discard(requirement)

    return tuple(dependency_order)


def parse(data: str) -> list[tuple[str, str]]:
    return list(map(lambda line: LINE_RE.match(line).groups(), data.split("\n")))


def _part_a(data: list[tuple[str, str]]) -> str:
    dependencies = {root: set() for root in [i for j in data for i in j]}
    for dependency, node in data:
        dependencies[node].add(dependency)

    order = solve_dependency_order(dependencies)
    return dependencies, "".join(order)


def part_a(data: list[tuple[str, str]]) -> str:
    _, order = _part_a(data)
    return order


def part_b(data):
    dependencies, order = _part_a(data)

    dependency_graph = deepcopy(dependencies)
    dependencies = set(dependencies.keys())
    jobs = []

    seconds = 0
    while dependencies:
        has_no_remaining_dep = set(
            filter(lambda dep: not dependency_graph[dep] and dep not in {req for req, _ in jobs}, dependencies)
        )

        for requirement in sorted(has_no_remaining_dep):
            if len(jobs) < 5:
                jobs.append((requirement, ord(requirement) - 4))

        jobs = [(requirement, remaining - 1) for requirement, remaining in jobs]
        seconds += 1

        for requirement, remaining in jobs:
            if remaining == 0:
                dependencies.remove(requirement)
                for req in dependency_graph:
                    dependency_graph[req].discard(requirement)

        jobs = [(requirement, remaining) for requirement, remaining in jobs if remaining != 0]

    return seconds


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day07.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 7 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=7, year=2018)

    print("Running day 7 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=7, year=2018)
