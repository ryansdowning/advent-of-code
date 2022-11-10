import math
from copy import deepcopy
from pathlib import Path
from statistics import quantiles, stdev
from time import perf_counter
from typing import Any, Callable


def format_time(seconds: float) -> str:
    if seconds > 1e0:
        return f"{seconds:.2f} sec"
    if seconds > 1e-3:
        return f"{int(seconds * 1e3)} ms"
    if seconds > 1e-6:
        return f"{int(seconds * 1e6)} μs"
    if seconds > 1e-9:
        return f"{int(seconds * 1e9)} ns"
    return str(seconds)


def timeit(func: Callable[..., Any], *args, max_time=15, **kwargs) -> tuple[float, list[float], Any]:
    runs = []

    args_copy = deepcopy(args)
    kwargs_copy = deepcopy(kwargs)
    start = perf_counter()
    result = func(*args_copy, **kwargs_copy)
    end = perf_counter()

    total_elapsed = end - start
    runs.append(total_elapsed)

    est_runs = max_time // total_elapsed
    if est_runs > 10:
        est_runs = 10 ** (math.floor(math.log10(est_runs))) - 1

    for _ in range(int(est_runs)):
        args_copy = deepcopy(args)
        kwargs_copy = deepcopy(kwargs)
        start = perf_counter()
        func(*args_copy, **kwargs_copy)
        end = perf_counter()
        elapsed = end - start

        runs.append(elapsed)
        total_elapsed += elapsed

    return total_elapsed, runs, result


def format_results(name, total_elapsed, runs, result=None, verbose=2):
    if verbose == 0:
        return ""

    n = len(runs)
    mu = total_elapsed / n
    std = stdev(runs) if len(runs) > 1 else 0
    name = f"{name}:"
    line1 = f"{name:<8}{format_time(mu):>8} ± {format_time(std):<8} per loop (mean ± std. dev. of {n} loops)"

    if verbose == 1:
        return line1

    low, high = min(runs), max(runs)
    low_o, *_, high_o = quantiles(runs, n=100)
    line2 = (
        f"min: {format_time(low):>5}, max: {format_time(high):>5}, "
        f"1%: {format_time(high_o):>5}, 99%: {format_time(low_o):>5}"
    )
    if verbose == 2:
        return f"{line1}\n{line2}"

    results_str = f"Result: {result}\n" if result is not None else ""
    return f"{results_str}{line1}\n{line2}"


def str_to_dir(path: str) -> Path:
    path = Path(path)
    if path.is_dir():
        return path
    raise ValueError(f"Unresolved path, could not locate directory at: {path}")


def str_to_file(path: str) -> Path:
    path = Path(path)
    if not path.exists():
        return path
    raise ValueError(f"Cannot create solution at: {path}, file already exists")
