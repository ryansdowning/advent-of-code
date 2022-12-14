import time
from copy import deepcopy

from aocd import submit

from pyutils import parsing, utils


def get_rocks(lines: list[list[tuple[int, int]]]) -> set[tuple[int, int]]:
    return {
        (x, y)
        for line in lines
        for (x1, y1), (x2, y2) in zip(line, line[1:])
        for x in range(min(x1, x2), max(x1, x2) + 1)
        for y in range(min(y1, y2), max(y1, y2) + 1)
    }


def parse(data):
    data = parsing.recursively_split(data, [("\n", None), (" -> ", None), (",", lambda x: tuple(map(int, x)))])
    return get_rocks(data)


def part_a(data):
    bottom = max(data, key=lambda x: x[1])[1]
    sand = set()
    void = False

    while not void:
        x, y = 500, 0
        falling = True
        while falling:
            if y > bottom:
                return len(sand)

            for xd, yd in [(0, 1), (-1, 1), (1, 1)]:
                xf, yf = x + xd, y + yd
                if (xf, yf) not in data and (xf, yf) not in sand:
                    x, y = xf, yf
                    break
            else:
                sand.add((x, y))
                if (x, y) == (500, 0):
                    void = True
                falling = False
                break


def part_b(data):
    bottom = max(data, key=lambda x: x[1])[1]
    sand = set()
    void = False

    while not void:
        x, y = 500, 0
        falling = True
        while falling:
            if y > bottom:
                sand.add((x, y))
                break

            for xd, yd in [(0, 1), (-1, 1), (1, 1)]:
                xf, yf = x + xd, y + yd
                if (xf, yf) not in data and (xf, yf) not in sand:
                    x, y = xf, yf
                    break
            else:
                sand.add((x, y))
                if (x, y) == (500, 0):
                    void = True
                falling = False
                break
    return len(sand)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day14.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 14 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=14, year=2022)

    print("Running day 14 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=14, year=2022)
