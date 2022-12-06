import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit
from rich.live import Live

from pyutils import utils


def parse(data):
    return data


# Rank: 1458
# def part_a(data):
#     for i, chr in enumerate(data):
#         if len(set(data[i:i+4])) == 4:
#             return i + 4

# Rank: 1085
# def part_b(data):
#     for i, chr in enumerate(data):
#         if len(set(data[i:i+14])) == 14:
#             return i + 14


def solution_no_viz(data: str, marker_len: int) -> int:
    marker = set()
    count = defaultdict(int)

    for chr in data[:marker_len]:
        count[chr] += 1
        marker.add(chr)

    for i, (chr0, chr1) in enumerate(zip(data, data[marker_len:]), marker_len):
        if len(marker) == marker_len:
            return i

        count[chr0] -= 1
        count[chr1] += 1

        marker.add(chr1)
        if count[chr0] == 0:
            marker.remove(chr0)


def solution_viz(data: str, marker_len: int) -> int:
    marker = set()
    count = defaultdict(int)

    with Live("", refresh_per_second=100) as live:
        for chr in data[:marker_len]:
            live.update(f"[red]{''.join(marker)}")
            count[chr] += 1
            marker.add(chr)
            time.sleep(0.001)

        for i, (chr0, chr1) in enumerate(zip(data, data[marker_len:]), marker_len):
            live.update(f"[red]{''.join(marker)}")
            if len(marker) == marker_len:
                live.update(f"[green]{''.join(marker)}")
                return i

            count[chr0] -= 1
            count[chr1] += 1

            marker.add(chr1)
            if count[chr0] == 0:
                marker.remove(chr0)
            time.sleep(0.001)


def solution(data: str, marker_len: int, viz: bool = False) -> int:
    if viz:
        return solution_viz(data, marker_len)
    return solution_no_viz(data, marker_len)


def part_a(data: str) -> int:
    return solution(data, 4)


def part_b(data: str) -> int:
    return solution(data, 14)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day06.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 6 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=6, year=2022)

    print("Running day 6 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=6, year=2022)
