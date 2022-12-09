"""
Day 1: Calorie Counting

This problem is split into two parts. The first part is to calculate the total
calories that each elf is carrying, an elfs inventory is seperated by a blank line \\n.

The second part is to calculate the total calories carried by the top three elves carrying
the most calories.
"""

from pathlib import Path

input_file = Path(__file__).parent.joinpath("inputs/day1.txt")
if not input_file.exists():
    print(
        f"Input file {input_file} does not exist, please create it in the inputs folder before running this script."
    )
    exit()

# Part 1
# The solution to part 1 is to calculate which elf is carrying the most calories
def part1(input_file=input_file):  #
    """
    This function calculates the total calories carried by each elf, then finds the elf with the most calories.

    Parameters
    ----------
    input_file : Path, optional
    """
    # Open the input file
    with open(input_file, "r") as f:
        # Read the input file
        input_data = f.read()
        # Split the input data into a list of lists
        input_data = [i.split("\n") for i in input_data.split("\n\n")]
        print(f"Part 1: There are {len(input_data)} elves.")
        # Sum each list to get the total calories for each elf, then find the max and it's index
        sum_calories = [sum([int(j) for j in i]) for i in input_data]
        max_calories = max(sum_calories)
        max_calories_index = sum_calories.index(max_calories)
        # Print the result
        print(
            f"Part 1: The elf with the most calories is {max_calories_index + 1} with {max_calories} calories."
        )
        return sum_calories


# Part 2
# The solution to part 2 is to calculate the top three elves with the most calories
def part2(sum_calories=None, input_file=input_file):
    """
    This function calculates the top three elves with the most calories.

    Parameters
    ----------
    sum_calories : list, optional
        A list of the total calories carried by each elf, by default None
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # If sum_calories is not provided, calculate it
    if sum_calories is None:
        sum_calories = part1(input_file=input_file)
    # Sort the list of calories in descending order
    sum_calories.sort(reverse=True)
    # Print the result
    print(
        f"Part 2: The top three elves have {sum_calories[0]} + {sum_calories[1]} + {sum_calories[2]} = {sum_calories[0] + sum_calories[1] + sum_calories[2]} calories."
    )
    return sum_calories[0] + sum_calories[1] + sum_calories[2]


if __name__ == "__main__":
    sum_calories = part1(input_file)
    part2(sum_calories=sum_calories, input_file=input_file)
