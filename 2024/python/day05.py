import time
from collections import defaultdict
from copy import deepcopy

from aocd import submit

from pyutils import parsing, utils


def parse(data):
    ordering_rules, updates = data.split("\n\n")
    ordering_rules = parsing.recursively_split(ordering_rules, [("\n", None), ("|", lambda x: list(map(int, x)))])
    updates = parsing.recursively_split(updates, [("\n", None), (",", lambda x: list(map(int, x)))])
    grouped_rules = defaultdict(lambda: {"before": set(), "after": set()})
    for before, after in ordering_rules:
        grouped_rules[before]["after"].add(after)
        grouped_rules[after]["before"].add(before)
    return grouped_rules, updates


def is_valid_update(update, grouped_rules):
    for i, before_page in enumerate(update):
        after = grouped_rules[before_page]["after"]
        for after_page in update[i + 1 :]:
            if after_page in after or before_page in grouped_rules[after_page]["before"]:
                continue
            return False
    return True


def part_a(data):
    grouped_rules, updates = data
    return sum(update[len(update) // 2] for update in updates if is_valid_update(update, grouped_rules))


def fix_update(update, grouped_rules):
    for i, before_page in enumerate(update):
        after = grouped_rules[before_page]["after"]
        for j, after_page in enumerate(update[i + 1 :], i + 1):
            if after_page in after or before_page in grouped_rules[after_page]["before"]:
                continue
            update[i], update[j] = update[j], update[i]

    return update if is_valid_update(update, grouped_rules) else fix_update(update, grouped_rules)


def part_b(data):
    grouped_rules, updates = data
    incorrect_updates = [update for update in updates if not is_valid_update(update, grouped_rules)]
    return sum(fix_update(update, grouped_rules)[len(update) // 2] for update in incorrect_updates)


if __name__ == "__main__":
    with open("/Users/ryan/hackathons/advent-of-code/inputs/2024/day05.txt", "r") as fp:
        data = fp.read().rstrip()

    data = parse(data)

    data_a = deepcopy(data)
    print("Running day 5 part A")
    start_a = time.perf_counter()

    solution_a = part_a(data_a)

    stop_a = time.perf_counter()
    elapsed_a = stop_a - start_a
    print(f"Part A finished in {utils.format_time(elapsed_a)} with solution: {solution_a}, submitting...")
    submit(solution_a, part="a", day=5, year=2024)
    print("Running day 5 part B")
    start_b = time.perf_counter()

    solution_b = part_b(data)

    stop_b = time.perf_counter()
    elapsed_b = stop_b - start_b
    print(f"Part B finished in {utils.format_time(elapsed_b)} with solution: {solution_b}, submitting...")
    submit(solution_b, part="b", day=5, year=2024)
