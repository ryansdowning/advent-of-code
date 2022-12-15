import re
import time
from copy import deepcopy
from dataclasses import dataclass

from aocd import submit

from pyutils import utils
from pyutils.algs import distance

LINE_RE = re.compile("Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


@dataclass(frozen=True)
class Sensor:
    x: int
    y: int
    bx: int
    by: int

    @property
    def dist(self):
        return distance.manhattan((self.x, self.y), (self.bx, self.by))


def parse(data):
    return list(map(lambda line: Sensor(*tuple(map(int, LINE_RE.match(line).groups()))), data.split("\n")))


def part_a(data):
    Y = 2000000
    possible = []
    for sensor in data:
        yd = abs(Y - sensor.y)
        if yd <= sensor.dist:
            xd = sensor.dist - yd
            possible.append((sensor.x - xd, sensor.x + xd))

    possible.sort()
    ranges = [possible[0]]
    for xr, yr in possible[1:]:
        if xr > ranges[-1][1]:
            ranges.append((xr, yr))
        else:
            ranges[-1] = (ranges[-1][0], max(ranges[-1][1], yr))

    return sum(yr - xr for xr, yr in ranges)


def part_b(data):
    Y = 4000000
    for y in range(0, Y):
        possible = []
        for sensor in data:
            yd = abs(y - sensor.y)
            if yd <= sensor.dist:
                xd = sensor.dist - yd
                possible.append((max(0, sensor.x - xd), min(Y, sensor.x + xd)))

        possible.sort()
        ranges = [possible[0]]
        for xr, yr in possible[1:]:
            if xr > ranges[-1][1]:
                ranges.append((xr, yr))
            else:
                ranges[-1] = (ranges[-1][0], max(ranges[-1][1], yr))

        if len(ranges) > 1 or (ranges[0][0] > 0 and ranges[0][1] > Y):
            if len(ranges) == 1:
                x = 0 if ranges[0][0] > 0 else Y
            else:
                x = ranges[0][1] + 1
            return x * Y + y


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day15.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 15 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=15, year=2022)

    print("Running day 15 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=15, year=2022)
