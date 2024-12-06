#
# File created on Wed Dec 04 2024 21:41:21 by T.Darnell
#
# The MIT License (MIT)
# Copyright (c) 2024 T.Darnell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import enum
import logging
from pathlib import Path
from typing import Generator
from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(day=int(Path(__file__).stem[3:]))


class SafetyFlags(enum.Enum):
    SAFE = 0
    UNSAFE_SIGN_CHANGE = 1
    UNSAFE_UNCHANGED = 2
    UNSAFE_THRESHOLD = 3


def check_safety(diffs: list[int]) -> SafetyFlags:
    if any(diff == 0 for diff in diffs):
        return SafetyFlags.UNSAFE_UNCHANGED
    max_diff: int = max(diffs)
    min_diff: int = min(diffs)
    if min_diff < 0 < max_diff:
        return SafetyFlags.UNSAFE_SIGN_CHANGE
    if min_diff < -3 or max_diff > 3:
        return SafetyFlags.UNSAFE_THRESHOLD
    return SafetyFlags.SAFE


@log_execution_time(logger=LOGGER)
def day02_part1(
    input_str="7 6 4 2 1\n1 2 7 8 9\n9 7 6 2 1\n1 3 2 4 5\n8 6 4 4 1\n1 3 6 7 9",
) -> int:
    safe = 0
    unsafe = 0
    lines: Generator[list[int]] = (
        list(map(int, line.split())) for line in input_str.splitlines()
    )
    for line in lines:
        diffs: list[int] = [line[i] - line[i - 1] for i in range(1, len(line))]
        flag: SafetyFlags = check_safety(diffs)
        LOGGER.debug(f"{line}: got safety flag of {flag}")
        if flag != SafetyFlags.SAFE:
            unsafe += 1
        else:
            safe += 1
    return safe


if __name__ == "__main__":
    input_str: str = read_day_input(int(Path(__file__).stem[3:]))
    LOGGER.setLevel(logging.DEBUG)  # uncomment to view where the unsafe lines are

    expected_solution: int = day02_part1()
    if expected_solution != 2:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of 2 for the provided worked example. Instead got: {expected_solution}"
        )

    part1_solution: int = day02_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")
