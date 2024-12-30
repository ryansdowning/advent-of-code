import time
from copy import deepcopy

from aocd import submit

from pyutils import utils

DIRECTIONS = {
    ">": (0, 1),
    "<": (0, -1),
    "^": (-1, 0),
    "v": (1, 0),
}


class Warehouse:
    def __init__(self, grid: str):
        self.grid = list(map(list, grid.splitlines()))
        self.rows = len(self.grid)
        self.columns = len(self.grid[0])

        self.boxes = set()
        self.robot = None
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == "O":
                    self.boxes.add((i, j))
                elif val == "@":
                    self.robot = (i, j)

    def is_wall(self, pos: tuple[int, int]):
        return self.grid[pos[0]][pos[1]] == "#"

    def is_direction_blocked(self, pos: tuple[int, int], direction: tuple[int, int]):
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if self.is_wall(new_pos):
            return True

        is_box = new_pos in self.boxes
        if not is_box:
            return False

        return self.is_direction_blocked(new_pos, direction)

    def _move_box(self, box: tuple[int, int], direction: tuple[int, int]):
        new_pos = (box[0] + direction[0], box[1] + direction[1])
        self.boxes.remove(box)
        if new_pos in self.boxes:
            self._move_box(new_pos, direction)
        self.boxes.add(new_pos)
        self.grid[new_pos[0]][new_pos[1]] = "O"

    def move_robot(self, direction: tuple[int, int]):
        if self.is_direction_blocked(self.robot, direction):
            return

        self.grid[self.robot[0]][self.robot[1]] = "."
        self.robot = (self.robot[0] + direction[0], self.robot[1] + direction[1])
        self.grid[self.robot[0]][self.robot[1]] = "@"
        if self.robot in self.boxes:
            self._move_box(self.robot, direction)

    def get_box_gps_coordinates(self):
        return [x * 100 + y for x, y in self.boxes]

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)


class WideWarehouse:
    def __init__(self, warehouse: Warehouse):
        output = [["*" for _ in range(warehouse.columns * 2)] for _ in range(warehouse.rows)]
        for i, row in enumerate(warehouse.grid):
            for j, val in enumerate(row):
                scaled_j = j * 2
                new_val = [val, val]
                if val == "@":
                    new_val = ["@", "."]
                elif val == "O":
                    new_val = ["[", "]"]
                output[i][scaled_j : scaled_j + 2] = new_val

        self.rows = warehouse.rows
        self.columns = warehouse.columns * 2
        self.grid = output
        self.boxes = set()
        self.robot = None
        for i, row in enumerate(self.grid):
            for j, val in enumerate(row):
                if val == "[" or val == "]":
                    self.boxes.add((i, j))
                elif val == "@":
                    self.robot = (i, j)

    def is_wall(self, pos: tuple[int, int]):
        return self.grid[pos[0]][pos[1]] == "#"

    def is_direction_blocked(self, pos: tuple[int, int], direction: tuple[int, int], checked_sibling=False):
        new_pos = (pos[0] + direction[0], pos[1] + direction[1])
        if self.is_wall(new_pos):
            return True

        is_box = new_pos in self.boxes
        if not is_box:
            return False

        blocked = False
        if checked_sibling or direction[0] == 0:
            pass
        elif self.grid[new_pos[0]][new_pos[1]] == "[":
            blocked = self.is_direction_blocked((pos[0], pos[1] + 1), direction, True)
        elif self.grid[new_pos[0]][new_pos[1]] == "]":
            blocked = self.is_direction_blocked((pos[0], pos[1] - 1), direction, True)

        return blocked or self.is_direction_blocked(new_pos, direction)

    def _move_box(self, box: tuple[int, int], direction: tuple[int, int], box_val: str, moved_sibling=False):
        if not moved_sibling and direction[0] != 0:
            connected_box = (box[0], box[1] + 1) if box_val == "[" else (box[0], box[1] - 1)
            connected_box_val = self.grid[connected_box[0]][connected_box[1]]
            self._move_box(connected_box, direction, connected_box_val, True)

        new_pos = (box[0] + direction[0], box[1] + direction[1])
        self.boxes.remove(box)

        if new_pos in self.boxes:
            self._move_box(new_pos, direction, self.grid[new_pos[0]][new_pos[1]])

        self.boxes.add(new_pos)
        self.grid[new_pos[0]][new_pos[1]] = box_val

    def move_robot(self, direction: tuple[int, int]):
        if self.is_direction_blocked(self.robot, direction):
            return

        self.grid[self.robot[0]][self.robot[1]] = "."
        self.robot = (self.robot[0] + direction[0], self.robot[1] + direction[1])
        original_value = self.grid[self.robot[0]][self.robot[1]]
        self.grid[self.robot[0]][self.robot[1]] = "@"
        if self.robot in self.boxes:
            self._move_box(self.robot, direction, original_value)

    def get_box_gps_coordinates(self):
        return [x * 100 + y for x, y in self.boxes if self.grid[x][y] == "["]

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)


def parse(data):
    #     data = """##########
    # #..O..O.O#
    # #......O.#
    # #.OO..O.O#
    # #..O@..O.#
    # #O#..O...#
    # #O..O..O.#
    # #.OO.O.OO#
    # #....O...#
    # ##########

    # <vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
    # vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
    # ><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
    # <<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
    # ^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
    # ^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
    # >^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
    # <><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
    # ^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
    # v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    warehouse, movements = data.split("\n\n")
    return Warehouse(warehouse), movements.replace("\n", "")


def part_a(data):
    warehouse, movements = data
    for movement in movements:
        direction = DIRECTIONS[movement]
        warehouse.move_robot(direction)

    return sum(warehouse.get_box_gps_coordinates())


def part_b(data):
    warehouse, movements = data
    warehouse = WideWarehouse(warehouse)
    print(warehouse)
    for movement in movements:
        direction = DIRECTIONS[movement]
        warehouse.move_robot(direction)
    print()
    print(warehouse)

    return sum(warehouse.get_box_gps_coordinates())


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day15.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 15 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    # submit(solution_a, part="a", day=15, year=2024)

    print("Running day 15 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=15, year=2024)
