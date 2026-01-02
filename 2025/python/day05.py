import bisect
import time
from copy import deepcopy
from typing import Sequence

from aocd import submit

from pyutils import utils


def parse(data: str) -> tuple[Sequence[Sequence[int]], list[int]]:
    ranges, ids = data.split("\n\n")
    parsed_ranges = [tuple(map(int, r.split("-"))) for r in ranges.split("\n")]
    sorted_ranges = sorted(parsed_ranges, key=lambda x: x[0])
    parsed_ids = list(map(int, ids.split("\n")))
    return sorted_ranges, parsed_ids


def part_a(data: tuple[Sequence[Sequence[int]], list[int]]) -> int:
    ranges, ids = data
    starts = [r[0] for r in ranges]
    count = 0
    for ingredient in ids:
        # Find index where ingredient would be inserted (ranges with start <= ingredient are before this)
        i = bisect.bisect_right(starts, ingredient)
        for j in range(i - 1, -1, -1):
            if ranges[j][1] >= ingredient:
                count += 1
                break
    return count


def get_maximal_ranges(ranges: Sequence[Sequence[int]]) -> Sequence[Sequence[int]]:
    maximal_ranges: set[tuple[int, int]] = set()
    for start, end in ranges:
        for m_start, m_end in maximal_ranges:
            # Is current range already encompassed?
            if m_start <= start and end <= m_end:
                break
            # Does the range fully encompass an existing maximal range?
            if start <= m_start and end >= m_end:
                maximal_ranges.remove((m_start, m_end))
                maximal_ranges.add((start, end))
                break
            # Does the range extend the upper bound of an existing maximal range?
            if m_end >= start and end > m_end:
                maximal_ranges.remove((m_start, m_end))
                maximal_ranges.add((m_start, end))
                break
            # Does the range extend the lower bound of an existing maximal range?
            if start < m_start and end <= m_start:
                maximal_ranges.remove((m_start, m_end))
                maximal_ranges.add((start, m_end))
                break
        # No overlaps found, add as new maximal range
        else:
            maximal_ranges.add((start, end))

    return list(maximal_ranges)


def part_b(data: tuple[Sequence[Sequence[int]], list[int]]) -> int:
    ranges, _ = data
    maximal_ranges = get_maximal_ranges(ranges)
    return sum(end - start + 1 for start, end in maximal_ranges)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2025/day05.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 5 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=5, year=2025)

    print("Running day 5 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=5, year=2025)
