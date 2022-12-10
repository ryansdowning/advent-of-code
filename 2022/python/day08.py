import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


def parse(data):
    return list(map(lambda x: list(map(int, x)), data.split("\n")))


def part_a(data):
    max_x, max_y = len(data), len(data[0])

    def can_be_seen(x, y):
        height = data[x][y]

        for x0 in range(0, x):
            if data[x0][y] >= height:
                break
        else:
            return True

        for x0 in range(x + 1, max_x):
            if data[x0][y] >= height:
                break
        else:
            return True

        for y0 in range(0, y):
            if data[x][y0] >= height:
                break
        else:
            return True

        for y0 in range(y + 1, max_y):
            if data[x][y0] >= height:
                break
        else:
            return True

        return False

    return sum(can_be_seen(x, y) for x in range(max_x) for y in range(max_y))


def part_b(data: list[list[int]]) -> int:
    max_x, max_y = len(data), len(data[0])

    def scenic_score(x, y):
        total_score = 1
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            score = 1
            x0, y0 = x, y
            while True:
                x0 += direction[0]
                y0 += direction[1]
                if x0 == 0 or x0 == max_x - 1 or y0 == 0 or y0 == max_y - 1:
                    break
                if not (0 <= x0 < max_x and 0 <= y0 < max_y) or data[x0][y0] >= data[x][y]:
                    break
                score += 1

            total_score *= score
        return total_score

    return max(scenic_score(x, y) for x in range(1, max_x - 1) for y in range(1, max_y - 1))


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day08.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 8 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=8, year=2022)

    print("Running day 8 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=8, year=2022)
