# Advent of Code

My attempts at advent of code over the years (not including 2019-2021 which are in independent repos).

### Prerequisites

- Get your advent of code session key from cookies and set it as an environment variable.

```bash
$ export AOC_SESSION=YOUR_TOKEN_HERE
```

### Run Day Solution

To test and submit python solutions run

```bash
$ uv run python -m [YYYY].python.day[dd]
```

Where `[YYYY]` is the 4 digit year and `[dd]` is the 2 digit day of month of the challenge

### Performance Runner

To test all python solutions with performance tests, run

```bash
$ uv run python -m pyutils.runner
```

_Optionally provide `-y` and `-d` to specify the year and list of days to run performance tests for._

### Starter Template

If you are using this repo as a template, the `start_day.py` file provides a quick way to get started for a given day's challenges, i.e:

```bash
$ uv run pyutils.start_day -y 2021 -d 1
```

Will download the inputs for day 1 of 2021 and create a `day01.py` file in `2021/python/` with a template to get started!
