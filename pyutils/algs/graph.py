from copy import deepcopy
from typing import Callable, TypeVar

T = TypeVar("T")


def solve_dependency_order(
    dependency_graph: dict[T, set[T]], sort_order: Callable[[set[T]], set[T]] = lambda x: x
) -> tuple[T]:
    """
    Generic dependency resolver using topological sort to determine the appropriate order of dependencies.

    Args:
        dependency_graph: An adjacency matrix where the keys are dependencies and the values are the dependencies which
          must come before them.
        sort_order: How to sort the order of dependencies when multiple are unconstrained on the same iteration. By
          default there is no sorting, and order can be unstable from the use of sets.

    Returns:
        Tuple of the dependencies where the order of the elements represents the resolved order of dependency execution.
    """
    dependency_graph = deepcopy(dependency_graph)
    dependencies = set(dependency_graph.keys())
    dependency_order = []

    while dependencies:  # Resolve dependencies as they are available.
        has_no_remaining_dep = set(filter(lambda dep: not dependency_graph[dep], dependencies))
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
            for req in dependency_graph:
                dependency_graph[req].discard(requirement)

    return tuple(dependency_order)
