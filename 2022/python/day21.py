import operator
import re
import time
from copy import deepcopy

from aocd import submit
from sympy import solve, sympify

from pyutils import utils
from pyutils.algs.graph import Graph

LINE_RE = re.compile(r"(.+) ([\-\*\/\+]) (.+)")
OPERATOR_MAP = {"+": operator.add, "-": operator.sub, "*": lambda a, b: a * b, "/": operator.floordiv}


def parse_line(line):
    name, yell = line.split(": ")
    if yell.isnumeric():
        return name, int(yell)
    return name, LINE_RE.match(yell).groups()


def parse(data):
    return dict(map(parse_line, data.split("\n")))


def part_a(data):
    graph = Graph({name: set() if isinstance(yell, int) else {yell[0], yell[2]} for name, yell in data.items()})
    values = {}
    order = graph.solve_dependency_order()
    for name in order:
        yell = data[name]
        if isinstance(yell, int):
            values[name] = yell
        else:
            values[name] = OPERATOR_MAP[yell[1]](values[yell[0]], values[yell[2]])
    return int(values["root"])


def depends_on(graph, node, target):
    return target in graph[node] or any(depends_on(graph, d, target) for d in graph[node])


def get_humn_expr(graph, data, values, node):
    if node == "humn":
        return node
    if not depends_on(graph, node, "humn"):
        return values[node]
    if isinstance(data[node], int):
        return data[node]
    left, op, right = data[node]
    return f"({get_humn_expr(graph, data, values, left)} {op} {get_humn_expr(graph, data, values, right)})"


def part_b(data):
    graph = Graph(
        {name: set() if isinstance(yell, int) else {yell[0], yell[2]} for name, yell in data.items() if name != "root"}
    )
    order = list(graph.solve_dependency_order())

    check1, _, check2 = data["root"]
    values = {}
    for name in order:
        yell = data[name]
        if isinstance(yell, int):
            values[name] = yell
        else:
            values[name] = OPERATOR_MAP[yell[1]](values[yell[0]], values[yell[2]])

    if depends_on(graph.graph, check1, "humn"):
        unknown = check1
        val = values[check2]
    else:
        unknown = check2
        val = values[check1]

    expr = f"{get_humn_expr(graph.graph, data, values, unknown)} - {val}"
    return int(solve(sympify(expr))[0])


if __name__ == "__main__":
    with open("/home/ryan/Desktop/repos/aoc/aoc-all/inputs/2022/day21.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 21 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=21, year=2022)

    print("Running day 21 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=21, year=2022)
