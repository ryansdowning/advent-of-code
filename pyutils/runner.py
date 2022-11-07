import argparse
import datetime
import glob
import os
import statistics
from functools import partial
from importlib import import_module
from pathlib import Path

from pyutils import utils

parser = argparse.ArgumentParser()
parser.add_argument("--days", "-d", type=int, nargs="*")
parser.add_argument("--year", "-y", type=int, default=datetime.datetime.now().year)
parser.add_argument("--verbose", "-v", action="count", default=1)
parser.add_argument("--max-time", "-m", type=int, default=15)
parser.add_argument("--solutions-dir", "-s", type=utils.str_to_dir)
parser.add_argument("--inputs-dir", "-i", type=utils.str_to_dir)
parser.add_argument("--package-name", "-p", type=str)

SOLUTION_PATTERN = "day*.py"

if __name__ == "__main__":
    args = parser.parse_args()
    days = args.days
    verbose = args.verbose

    inputs_dir = args.inputs_dir
    if inputs_dir is None:
        inputs_dir = Path(__file__).parent.parent.resolve() / f"inputs/{args.year}"

    solutions_dir = args.solutions_dir
    if solutions_dir is None:
        solutions_dir = Path(__file__).parent.parent.resolve() / f"{args.year}/python/"

    pkg_name = args.package_name
    if pkg_name is None:
        pkg_name = f"{args.year}.python"

    MODULES = {}
    for file in glob.glob(str(solutions_dir / SOLUTION_PATTERN)):
        stem = Path(file).stem
        MODULES[stem] = import_module(f"{pkg_name}.{stem}", pkg_name)
    MODULES = sorted(((stem, module) for stem, module in MODULES.items()), key=lambda x: x[0])
    print(f"Starting runner for {args.year}")

    for stem, module in MODULES:
        day = int(stem[-2:])
        if days and day not in days:
            continue
        print(f"Running day {day}")

        with open(inputs_dir / f"{stem}.txt", "r") as fp:
            time, runs, data = utils.timeit(lambda: fp.read().strip(), max_time=args.max_time)
        print(utils.format_results("Reading", time, runs, verbose=verbose))

        time, runs, data = utils.timeit(module.parse, data=data, max_time=args.max_time)
        n = len(runs)
        print(utils.format_results("Parsing", time, runs, verbose=verbose))

        time, runs, solution_a = utils.timeit(module.part_a, data=data, max_time=args.max_time)
        print(utils.format_results("Part A", time, runs, solution_a, verbose=verbose))

        time, runs, solution_b = utils.timeit(module.part_b, data=data, max_time=args.max_time)
        print(utils.format_results("Part B", time, runs, solution_b, verbose=verbose))

        print()
