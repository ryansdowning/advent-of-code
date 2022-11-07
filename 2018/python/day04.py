import datetime
import re
import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import utils

RE_START_SHIFT = re.compile(r"Guard #(\d+) begins shift")


def parse_line(data: str) -> tuple[datetime.datetime, str]:
    date, msg = data.split("] ")
    return datetime.datetime.strptime(date, "[%Y-%m-%d %H:%M"), msg


def parse(data: str) -> dict[int, list[tuple[datetime.date, int, int]]]:
    data = list(map(parse_line, data.split("\n")))
    data = sorted(data, key=lambda x: x[0])

    sleep_intervals: dict[int, list[tuple[datetime.date, int, int]]] = defaultdict(list)
    curr_guard = None
    start_sleep = None
    for time, event in data:
        if (guard := RE_START_SHIFT.match(event)) is not None:
            curr_guard = int(guard.group(1))
        elif event == "falls asleep":
            start_sleep = time.minute
        elif event == "wakes up":
            sleep_intervals[curr_guard].append((time.date, start_sleep, time.minute))

    return sleep_intervals


def get_minute_sleep_frequency(intervals: list[datetime.date, int, int]) -> list[int]:
    sleep_tracker = [0 for _ in range(60)]
    for _, a, b in intervals:
        for i in range(a - 1, b - 1):
            sleep_tracker[i] += 1
    return sleep_tracker


def part_a(data: dict[int, list[tuple[datetime.date, int, int]]]) -> int:
    total_sleep = {guard: sum(b - a for (_, a, b) in intervals) for guard, intervals in data.items()}
    sleepy_guard = max(total_sleep, key=total_sleep.get)

    sleep_frequency = get_minute_sleep_frequency(data[sleepy_guard])
    sleepy_minute = max(range(60), key=sleep_frequency.__getitem__) + 1

    return sleepy_guard * sleepy_minute


def part_b(data: dict[int, list[tuple[datetime.date, int, int]]]) -> int:
    sleep_frequencies = {guard: get_minute_sleep_frequency(intervals) for guard, intervals in data.items()}
    max_frequencies = {guard: max(frequencies) for guard, frequencies in sleep_frequencies.items()}
    sleepy_guard = max(max_frequencies, key=max_frequencies.get)
    sleepy_minute = max(range(60), key=sleep_frequencies[sleepy_guard].__getitem__) + 1
    return sleepy_guard * sleepy_minute


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2018/day04.txt", "r") as fp:
        data = fp.read().strip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 4 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=4, year=2018)

    print("Running day 4 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=4, year=2018)
