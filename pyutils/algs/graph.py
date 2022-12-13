from copy import deepcopy
from typing import Callable, TypeVar

T = TypeVar("T")

import heapq
from typing import Callable, TypeVar

T = TypeVar("T")


class Graph:
    def __init__(self, graph: dict[T, set[T]]):
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

    def solve_dependency_order(self, sort_order: Callable[[set[T]], set[T]] = lambda x: x) -> tuple[T]:
        """
        Generic dependency resolver using topological sort to determine the appropriate order of dependencies.

        The graph represents an adjacency list where the keys are dependencies and the values are the dependencies which
        must come before them.

        Args:
            sort_order: How to sort the order of dependencies when multiple are unconstrained on the same iteration. By
            default there is no sorting, and order can be unstable from the use of sets.

        Returns:
            Tuple of the dependencies where the order of the elements represents the resolved order of dependency execution.
        """
        graph = deepcopy(self.graph)
        dependencies = set(graph.keys())
        dependency_order = []

        while dependencies:  # Resolve dependencies as they are available.
            has_no_remaining_dep = set(filter(lambda dep: not graph[dep], dependencies))
            # If there are no dependencies that can be resolved, then the dependency cannot be solved, cycle exists.
            if not has_no_remaining_dep:
                raise ValueError(
                    f"Could not resolve the remaining dependencies: {dependencies}. There is probably a cycle in the "
                    f"dependencies which is impossible to solve."
                )

            for requirement in sort_order(has_no_remaining_dep):
                dependency_order.append(requirement)
                dependencies.remove(requirement)
                # After resolving dependency, remove it from the dependencies of all other features.
                for req in graph:
                    graph[req].discard(requirement)

        return tuple(dependency_order)
