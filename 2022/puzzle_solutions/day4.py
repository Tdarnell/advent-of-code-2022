"""
Day 4: Camp Cleanup

Every section has a unique ID number, and each Elf is assigned a range of section IDs.

they've noticed that many of the assignments overlap

To try to quickly find overlaps and reduce duplicated effort, the Elves pair up
and make a big list of the section assignments for each pair (your puzzle input).
"""

from pathlib import Path

input_file = Path("inputs/2022/day4.txt")
if not input_file.exists():
    print(
        f"Input file {input_file} does not exist, please create it in the inputs folder before running this script."
    )
    exit()

# Part 1
# In how many assignment pairs does one range fully contain the other?
def part1(input_file=input_file):
    """
    This function calculates how many assignment pairs overlap.

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # Open the input file
    with open(input_file, "r") as f:
        # Read the input file
        input_data = f.read()
        # Split the input data into a list of lists
        input_data = [i.replace(",", "-").split("-") for i in input_data.splitlines()]
        # Now we have a list of lists, each list contains 4 items
        # The next step is to create a list of bools, where either
        # [0] <= [2] and [1] >= [3] or [0] >= [2] and [1] <= [3]
        # If the bool is True, then the ranges overlap
        # If the bool is False, then the ranges do not overlap
        overlaps = []
        for i in input_data:
            if (int(i[0]) <= int(i[2]) and int(i[1]) >= int(i[3])) or (
                int(i[0]) >= int(i[2]) and int(i[1]) <= int(i[3])
            ):
                overlaps.append(True)
            else:
                overlaps.append(False)
        # Print the result
        print(f"Part 1: There are {sum(overlaps)} overlapping assignment pairs.")
        return input_data


# Part 2
# How many assignment pairs overlap at all?
def part2(input_data=None, input_file=input_file):
    """
    This function calculates how many assignment pairs overlap at all.

    Parameters
    ----------
    input_data : list, optional
        A list of the assignment pairs, by default None
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # If input_data is not provided, calculate it
    if input_data is None:
        input_data = part1(input_file=input_file)
    # Now we have a list of lists, each list contains 4 items
    # The next step is to create a list of bools, where the ranges overlap at all
    # For this we can compare the ranges in the following way:
    # a start value ([0 or 2]) is bigger than the other start value but smaller thant the other end ([3 or 1])
    # or the other way around, an end value ([1 or 3]) is bigger than the other start value but smaller thant the other end ([3 or 1])
    # If the bool is True, then the ranges overlap
    # If the bool is False, then the ranges do not overlap
    overlaps = []
    for i in input_data:
        checks = [
            int(i[0]) >= int(i[2]) and int(i[0]) <= int(i[3]),
            int(i[1]) >= int(i[2]) and int(i[1]) <= int(i[3]),
            int(i[2]) >= int(i[0]) and int(i[2]) <= int(i[1]),
            int(i[3]) >= int(i[0]) and int(i[3]) <= int(i[1]),
        ]
        if any(checks):
            overlaps.append(True)
        else:
            overlaps.append(False)
    # Print the result
    print(f"Part 2: There are {sum(overlaps)} overlapping assignment pairs.")


if __name__ == "__main__":
    result = part1()
    part2(input_data=result)
