#
# File created on Wed Dec 04 2024 20:32:52 by T.Darnell
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
import logging
from pathlib import Path
from typing import Generator
from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(day=int(Path(__file__).stem[3:]))


@log_execution_time(logger=LOGGER)
def day01_part1(
    input_str: str = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3",
) -> int:
    """
    Solve part 1 of the puzzle. This problem requires sorting the two columns then summing the result.

    Parameters
    ----------
    input_str : str, optional
        The input data for the puzzle.

    Returns
    -------
    int
        The solution to part 1 of the puzzle.
    """
    lines: Generator[tuple[int, ...], None, None] = (
        tuple(map(int, _.split())) for _ in input_str.splitlines()
    )
    col1, col2 = zip(*lines)
    # the problem asks us to sum the smallest elements from each list recursively
    # this is easily achieved by sorting
    col1, col2 = sorted(col1), sorted(col2)
    diff: int = sum(abs(c1 - c2) for c1, c2 in zip(col1, col2))
    return diff


@log_execution_time(logger=LOGGER)
def day01_part2(
    input_str: str = "3   4\n4   3\n2   5\n1   3\n3   9\n3   3",
) -> int:
    """
    Solve part 2 of the puzzle. This problem requires the calculation of a 'similarity' score between the two lists.

    Parameters
    ----------
    input_str : str, optional
        The input data for the puzzle.

    Returns
    -------
    int
        The solution to part 2 of the puzzle.
    """
    lines: Generator[tuple[int, ...], None, None] = (
        tuple(map(int, _.split())) for _ in input_str.splitlines()
    )
    col1, col2 = zip(*lines)
    # building a dict of col2 unique items, and their respective counts from the list object
    col2_counts = {k: col2.count(k) for k in list(set(col2))}
    # similarity is given as the multiple of each element in column 1 by it's count in column 2
    # the dict lets us look this up quickly
    similarity = sum([c * col2_counts.get(c, 0) for c in col1])
    return similarity


if __name__ == "__main__":
    expected_solution: int = day01_part1()
    if expected_solution != 11:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of 11 for the provided worked example. Instead got: {expected_solution}"
        )

    input_str = read_day_input(day=1)
    part1_solution: int = day01_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution = day01_part2()
    if expected_solution != 31:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of 31 for the provided worked example. Instead got: {expected_solution}"
        )

    part2_solution: int = day01_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
