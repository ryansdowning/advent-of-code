import time
from copy import deepcopy

from aocd import submit

from pyutils import utils


class Block:
    def __init__(self, id: int, file_size: int, free: int):
        self.file_size = file_size
        self.files = [id for _ in range(file_size)]
        self.free = free


class Disk:
    def __init__(self, data):
        data_len = len(data)
        self.blocks = [
            Block(id, int(data[i]), int(data[i + 1]) if i + 1 < data_len else 0)
            for id, i in enumerate(range(0, len(data), 2))
        ]

    def get_tape(self):
        out = []
        for block in self.blocks:
            out.extend(block.files)
            out.extend(["."] * block.free)
        return out

    def get_checksum(self):
        return sum(id * i for i, id in enumerate(self.get_tape(), 0) if id != ".")


def parse(data):
    return Disk(data)


def part_a(data: Disk):
    left = 0
    right = len(data.blocks) - 1
    while left < right:
        left_block, right_block = data.blocks[left], data.blocks[right]
        if left_block.free >= right_block.file_size:
            left_block.files.extend(right_block.files)
            left_block.free -= len(right_block.files)
            right_block.files = []
        else:
            left_block.files.extend(right_block.files[: left_block.free])
            right_block.files = right_block.files[left_block.free :]
            left_block.free = 0

        if left_block.free == 0:
            left += 1
        if len(right_block.files) == 0:
            right -= 1

    return data.get_checksum()


def part_b(data: Disk):
    lowest_free_block = 0
    for i in range(len(data.blocks) - 1, 0, -1):
        block = data.blocks[i]

        for j in range(lowest_free_block, i):
            free_block = data.blocks[j]
            if free_block.free >= block.file_size:
                free_block.files.extend(block.files[: block.file_size])
                free_block.free -= block.file_size
                if lowest_free_block == j and free_block.free == 0:
                    lowest_free_block += 1
                block.files = ["."] * block.file_size + block.files[block.file_size :]
                break

    return data.get_checksum()


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day09.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 9 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=9, year=2024)

    print("Running day 9 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=9, year=2024)
