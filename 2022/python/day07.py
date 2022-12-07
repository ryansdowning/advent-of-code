import time
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Optional

from aocd import submit

from pyutils import utils


@dataclass(frozen=True)
class File:
    name: str
    size: int


@dataclass
class Filesystem:
    name: str
    parent: Optional["Filesystem"] = None
    dirs: list["Filesystem"] = field(default_factory=list)
    files: set[File] = field(default_factory=set)

    def get_dir(self, name: str) -> "Filesystem":
        for filesystem in self.dirs:
            if filesystem.name == name:
                return filesystem
        filesystem = Filesystem(name, self)
        self.dirs.append(filesystem)
        return filesystem

    def get_total_size(self):
        total = sum(file.size for file in self.files)
        return total + sum(filesystem.get_total_size() for filesystem in self.dirs)

    def get_sizes(self):
        sizes = [self.get_total_size()]
        for filesystem in self.dirs:
            sizes.extend(filesystem.get_sizes())
        return sizes


def parse(data: str) -> Filesystem:
    data = data.split("$ ")[1:]
    root_filesystem = Filesystem("")
    curr_filesystem = root_filesystem

    for cmd in data:
        if cmd.startswith("cd"):
            arg = cmd.strip().split(" ")[1]
            if arg == "/":
                curr_filesystem = root_filesystem
            elif arg == "..":
                curr_filesystem = curr_filesystem.parent
            else:
                curr_filesystem = curr_filesystem.get_dir(arg)
        else:
            lst = cmd.strip().split("\n")[1:]
            for file in lst:
                if not file.startswith("dir"):
                    size, file = file.split(" ")
                    curr_filesystem.files.add(File(file, int(size)))

    return root_filesystem


def part_a(data: Filesystem) -> int:
    return sum(size for size in data.get_sizes() if size <= 100000)


def part_b(data):
    TOTAL_SPACE = 70000000
    REQUIRED_SPACE = 30000000
    used_space = data.get_total_size()
    diff = max(0, REQUIRED_SPACE - (TOTAL_SPACE - used_space))
    return min(size for size in data.get_sizes() if size >= diff)


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day07.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 7 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=7, year=2022)

    print("Running day 7 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=7, year=2022)
