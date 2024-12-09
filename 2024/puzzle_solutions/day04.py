#
# File created on Sun Dec 08 2024 17:09:35 by T.Darnell
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
from typing import Any, Iterable
from common_utils import log_execution_time, set_up_logger, read_day_input
import numpy as np

LOGGER: logging.Logger = set_up_logger(day=int(Path(__file__).stem[3:]))


def get_diagonals(mat: np.ndarray) -> list[np.ndarray]:
    """
    Get all of the diagonal elements of a matrix, starting from bottom left to top right

    Parameters
    ----------
    mat : np.ndarray
        The input matrix to extract diagonals from,
        flip this if you want the backwards (bottom right to top left)

    Returns
    -------
    list[np.ndarray]
        A list of arrays containing the diagonal elements,
        starting from the bottom left of the input matrix and ending at the top right
    """
    return [mat.diagonal(i) for i in range(-mat.shape[0] + 1, mat.shape[1])]


def pad_to_length(arr: Iterable, length: int, pad_with: Any = 0) -> np.ndarray:
    """
    Pad array elements to a fixed length
    (used for creating an array from the diagonals which are uneven length)

    Parameters
    ----------
    arr : np.ndarray or list[np.ndarray]
        The input array to pad, must be an iterable type
    length : int
        The fixed length to pad the array elements to

    Returns
    -------
    np.ndarray
        An array of the input elements padded to the fixed length
    """
    return np.array(
        [
            np.pad(a, (0, length - len(a)), "constant", constant_values=pad_with)
            for a in arr
        ]
    )


class Directions(enum.Enum):
    ROWS = 0
    COLUMNS = 1
    FORWARDS_DIAGONALS = 2
    BACKWARDS_DIAGONALS = 3


def get_padded_arrays(
    lines: tuple[int],
    directions: list[Directions] = [
        Directions.ROWS,
        Directions.COLUMNS,
        Directions.FORWARDS_DIAGONALS,
        Directions.BACKWARDS_DIAGONALS,
    ],
) -> tuple[np.ndarray, dict]:
    """
    Get all of the padded arrays from the input lines

    Parameters
    ----------
    lines : tuple[int]
        The input lines to extract arrays from
    directions : list[Directions], optional
        The directions to extract arrays from, by default all directions are selected

    Returns
    -------
    tuple[np.ndarray, dict]
        A tuple containing the combined arrays and their indexes
    """
    mat = np.array(list(lines), dtype=np.int8)
    arrays = []
    indexes = {}

    # extract all selected directions
    if Directions.ROWS in directions:
        rows = mat
        arrays.append(rows)
        indexes["rows"] = rows.shape[0]
    if Directions.COLUMNS in directions:
        columns = mat.T
        arrays.append(columns)
        indexes["columns"] = columns.shape[0]
    if Directions.FORWARDS_DIAGONALS in directions:
        forward_diagonals = [
            mat.diagonal(i) for i in range(-mat.shape[0] + 1, mat.shape[1])
        ]
        arrays.append(forward_diagonals)
        indexes["forward_diagonals"] = max(len(d) for d in forward_diagonals)
    if Directions.BACKWARDS_DIAGONALS in directions:
        backward_diagonals = [
            np.fliplr(mat).diagonal(i) for i in range(-mat.shape[0] + 1, mat.shape[1])
        ]
        arrays.append(backward_diagonals)
        indexes["backward_diagonals"] = max(len(d) for d in backward_diagonals)

    # Determine the maximum length for padding from all selected directions
    max_len = max(indexes.values())

    # Combine and pad all arrays to the maximum length so an array can be returned
    combined = np.vstack(tuple(pad_to_length(a, max_len) for a in arrays))

    return combined, indexes


@log_execution_time(logger=LOGGER)
def day04_part1(
    input_str: str = "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX",
) -> int:
    """
    Count the number of 'XMAS' in the input string in any direction (rows, columns, diagonals and inverse of each)

    Parameters
    ----------
    input_str : str
        The input string to search for 'XMAS' in

    Returns
    -------
    int
        The number of 'XMAS' found in the input string
    """
    # Convert each line of the input string to a tuple of integers based on the mapping
    mapping: dict[str, int] = {"X": 1, "M": 2, "A": 3, "S": 4}
    lines = (tuple(mapping[c] for c in b) for b in input_str.splitlines())

    # Get the padded arrays and their indexes, this was changed to a
    # re-usable function during solving part 2
    combined, indexes = get_padded_arrays(lines)

    # Log the indexes of the combined arrays, if we needed to reverse engineer
    # positions of "XMAS" in part 2 this was my planned method
    LOGGER.debug(f"Indexes in combined list of len {len(combined)} are:")
    for k, v in indexes.items():
        LOGGER.debug((k, v))

    # Define the search keys to look for in the arrays
    search_keys = ([1, 2, 3, 4], [4, 3, 2, 1])
    search_keys_set = {tuple(key) for key in search_keys}

    count = 0
    # Iterate over each row in the combined arrays
    for row in combined:
        for start in range(len(row) - 3):
            # Check for the presence of search keys in the row
            if tuple(row[start : start + 4]) in search_keys_set:
                count += 1
    return count


@log_execution_time(logger=LOGGER)
def day04_part2(
    input_str: str = "MMMSXXMASM\nMSAMXMSMSA\nAMXSXMAAMM\nMSAMASMSMX\nXMASAMXAMM\nXXAMMXXAMA\nSMSMSASXSS\nSAXAMASAAA\nMAMMMXMMMM\nMXMXAXMASX",
) -> int:
    """
    Find the number of X shaped 'MAS' in the input string

    Parameters
    ----------
    input_str : str
        The input string to search for X shaped 'MAS' in

    Returns
    -------
    int
        The number of X shaped 'MAS' found in the input string
    """
    mapping: dict[str, int] = {"X": 1, "M": 2, "A": 3, "S": 4}
    lines = list(tuple(mapping[c] for c in b) for b in input_str.splitlines())

    # get only the forward diagonals as we are looking for an X shape
    forward_diagonals, indexes = get_padded_arrays(
        lines,
        directions=[Directions.FORWARDS_DIAGONALS],
    )

    # forward_diagonals = combined[0 : indexes["forward_diagonals"] * 2 - 1]
    # backward_diagonals = combined[indexes["forward_diagonals"] * 2 - 1 :]
    # LOGGER.debug(forward_diagonals)
    # LOGGER.debug(backward_diagonals)

    search_keys = ([2, 3, 4], [4, 3, 2])
    search_keys_set = {tuple(key) for key in search_keys}
    count = 0

    # Iterate over each row in the combined arrays
    for i, row in enumerate(forward_diagonals, start=1):
        if i in [1, 2, len(forward_diagonals), len(forward_diagonals) - 1]:
            # impossible for an X shape to form here as the diagonals are on the corners
            # we could equally check the non-zero count is > 2
            continue
        for start in range(len(row) - 2):
            # Check for the presence of search keys in the row
            if tuple(row[start : start + 3]) in search_keys_set:
                # calculate the row and column number of the top left corner of the X shape
                row_num_top_left = -i + start
                col_num_top_left = 0 + start
                if i > len(lines):
                    # we are past the middle of the matrix, so the row no longer decreases and
                    # the column number increases instead
                    LOGGER.debug("Right hand corner")
                    row_num_top_left = 0 + start
                    col_num_top_left = len(row) - np.count_nonzero(row[start:])
                LOGGER.debug(
                    f"({row_num_top_left=}, {col_num_top_left=}) [{start=}, {row=}]"
                )
                original_row = lines[row_num_top_left]
                LOGGER.debug(original_row)
                LOGGER.debug(
                    f"Value on diagonal: {row[start]}, Value on original row: {original_row[col_num_top_left]} ({row_num_top_left=},{col_num_top_left=})"
                )
                top_right_corner = original_row[col_num_top_left + 2]
                bottom_left_corner = lines[row_num_top_left + 2][col_num_top_left]
                if (top_right_corner, bottom_left_corner) in [(2, 4), (4, 2)]:
                    count += 1
                    # LOGGER.debug(row)
                    # LOGGER.debug(original_row)
                    # if tuple(backward_diagonals[i][start : start + 3]) in search_keys_set:
                    # count += 1

    return count


if __name__ == "__main__":
    input_str = read_day_input(int(Path(__file__).stem[3:]))
    # LOGGER.setLevel(logging.DEBUG)  # uncomment to view where the unsafe lines are

    expected_value: int = 18
    test_solution: int = day04_part1()
    if test_solution != expected_value:
        LOGGER.error(
            f"Problem with solution to part 1! Did not get the expected answer of {expected_value} for the provided worked example. Instead got: {test_solution}"
        )

    part1_solution: int = day04_part1(input_str)
    LOGGER.info(f"Part 1 solution: {part1_solution}")

    expected_value: int = 9
    test_solution: int = day04_part2()
    if test_solution != expected_value:
        LOGGER.error(
            f"Problem with solution to part 2! Did not get the expected answer of {expected_value} for the provided worked example. Instead got: {test_solution}"
        )

    part2_solution: int = day04_part2(input_str)
    LOGGER.info(f"Part 2 solution: {part2_solution}")
