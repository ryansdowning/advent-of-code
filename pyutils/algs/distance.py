import math


def manhattan(a: tuple[int | float, int | float], b: tuple[int | float, int | float]) -> int | float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def euclidean(a: tuple[int | float, int | float], b: tuple[int | float, int | float]) -> int | float:
    return math.sqrt(((a[0] - b[0]) ** 2) + ((a[1] - b[1]) ** 2))
