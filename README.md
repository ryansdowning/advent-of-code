# Advent of Code 2021

Completed AOC 2021 challenges using Python 3 and OCaml (hopefully :)

### Run Day Solution

Prerequisite: get advent of code session key from cookies and set it as an environment variable

```bash
$ export AOC_SESSION=YOUR_TOKEN_HERE
```

To test python solutions run

```bash
$ cd python/
$ poetry run python -m solutions.dayXX
```
Where `XX` is the day of the challenge

### Performance Runner

To test all python solutions with performance tests, run

```bash
$ poetry run python -m pyutils.runner
```

### Starter Template

If you are using this repo as a template, the `start_day.py` file provides a quick way to get started for a given day's challenges, i.e:

```bash
$ poetry run pyutils.start_day -y 2021 -d 1
```

Will download the inputs for day 1 of 2021 and create a `day01.py` file in `python/solutions/` with a template to get started!

