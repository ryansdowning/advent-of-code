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
    data = list(map(lambda line: LINE_RE.match(line).groups(), data.split("\n")))

    dependencies = {root: set() for root in [i for j in data for i in j]}
    for dependency, node in data:
        dependencies[node].add(dependency)
    return dependencies


def part_a(data: dict[str, set[str]]) -> str:
    return "".join(solve_dependency_order(data))


def part_b(data: dict[str, set[str]]):
    dependency_graph = deepcopy(data)
    dependencies = set(data.keys())
    jobs = {}

    seconds = 0
    while dependencies:
        has_no_remaining_dep = set(filter(lambda dep: not dependency_graph[dep] and dep not in jobs, dependencies))

        for requirement in sorted(has_no_remaining_dep):
            if len(jobs) < 5:
                jobs[requirement] = seconds + ord(requirement) - 4

        seconds += 1
        for requirement, finish in list(jobs.items()):
            if finish <= seconds:
                jobs.pop(requirement)
                dependencies.remove(requirement)
                for req in dependency_graph:
                    dependency_graph[req].discard(requirement)

        # jobs = [(requirement, remaining) for requirement, remaining in jobs if remaining != 0]

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
