#
# File created on Fri Dec 06 2024 00:09:57 by T.Darnell
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
import re
from common_utils import log_execution_time, set_up_logger, read_day_input

LOGGER: logging.Logger = set_up_logger(day=int(Path(__file__).stem[3:]))


@log_execution_time(logger=LOGGER)
def day03_part1(
    input_str="xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))",
) -> int:
    regex_pattern = r"mul\((\d+),(\d+)\)"
    result = 0
    for match in re.finditer(regex_pattern, input_str):
        int1 = int(match.group(1))
        int2 = int(match.group(2))
        result += int1 * int2
        LOGGER.debug(f"Found ints {int1}, {int2} which multiply to {(int1*int2)=}")
    return result


@log_execution_time(logger=LOGGER)
def day03_part2(
    input_str="xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))",
) -> int:
    regex_pattern = r"mul\((\d+),(\d+)\)"
    result = 0
    input_strs_donts = input_str.split(("don't()"))
    input_strs_dos = "".join(
        [
            "".join(str(dont).split("do()")[1:])
            for dont in input_strs_donts[1:]
            if "do()" in dont
        ]
    )
    input_strs_dos = input_strs_donts[0] + input_strs_dos
    for match in re.finditer(regex_pattern, input_strs_dos):
        int1 = int(match.group(1))
        int2 = int(match.group(2))
        result += int1 * int2
        LOGGER.debug(f"Found ints {int1}, {int2} which multiply to {(int1*int2)=}")
    return result


if __name__ == "__main__":
    input_str = read_day_input(int(Path(__file__).stem[3:]))
    # LOGGER.setLevel(logging.DEBUG)  # uncomment to view where the unsafe lines are

    expected_solution: int = day03_part1()
    if expected_solution != 161:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of 161 for the provided worked example. Instead got: {expected_solution}"
        )

    part1_solution: int = day03_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_solution: int = day03_part2()
    if expected_solution != 48:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of 48 for the provided worked example. Instead got: {expected_solution}"
        )

    part2_solution: int = day03_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
