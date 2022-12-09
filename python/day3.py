"""
Day 3: Rucksack Reorganization

Each rucksack has two large compartments.

Case sensitive input a != A.

The list of items for each rucksack is given as characters all on a single line.
A given rucksack always has the same number of items in each of its two compartments, 
so the first half of the characters represent items in the first compartment, 
while the second half of the characters represent items in the second compartment.

To help prioritize item rearrangement, every item type can be converted to a priority:
Lowercase item types a through z have priorities 1 through 26.
Uppercase item types A through Z have priorities 27 through 52.
"""

from pathlib import Path

input_file = Path(__file__).parent.joinpath("inputs/day3.txt")
if not input_file.exists():
    print(
        f"Input file {input_file} does not exist, please create it in the inputs folder before running this script."
    )
    exit()

# Map the priorities of each item type
item_priorities = {
    chr(97 + i): i + 1 for i in range(26)
}  # Lowercase item types a through z have priorities 1 through 26.
item_priorities.update(
    {chr(65 + i): i + 27 for i in range(26)}
)  # Uppercase item types A through Z have priorities 27 through 52.

# Part 1
# Find the item type that appears in both compartments of each rucksack. What is the sum of the priorities of those item types?
def part1(input_file=input_file):
    """
    Function to calculate the sum of the priorities of the items that appear in both compartments of each rucksack.

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # Open the input file
    with open(input_file, "r") as f:
        # Read the input file
        input_data = f.read()
        print([len(i)/2 for i in input_data.splitlines()])
        # Split the input data into a list of lists
        input_data = [(i[:int(len(i)/2)], i[int(len(i)/2):]) for i in input_data.splitlines()]
        print(f"Part 1: There are {len(input_data)} rucksacks.")
        # Now find the common items in each rucksack
        common_items = [set(i[0]).intersection(set(i[1])) for i in input_data]
        # Now find the sum of the priorities of the common items
        sum_priorities = sum([sum([item_priorities[i] for i in j]) for j in common_items])
        # Print the result
        print(f"Part 1: The sum of the priorities of the common items is {sum_priorities}.")
        return input_data

# Part 2
# Now the rucksacks are split into groups of 3. Find the item type that appears in all 3 compartments of each rucksack. What is the sum of the priorities of those item types?
def part2(input_data=None, input_file=input_file):
    """
    Function to calculate the sum of the priorities of the items that appear in all 3 compartments of each rucksack.

    Parameters
    ----------
    input_data : list, optional
        A list of the items in each rucksack, by default None
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # If the input data is not provided, calculate it
    if input_data is None:
        input_data = part1(input_file)
    grouped = []
    # Split the input data into a list of lists of 3
    for i in range(0, len(input_data), 3):
        group = [''.join(i) for i in input_data[i : i + 3]]
        # Now find the common items in all 3 rucksacks
        common_item = set(group[0]).intersection(set(group[1])).intersection(set(group[2])).pop()
        # Now add the common items to the grouped dictionary
        grouped.append(common_item)
    print(f"Part 2: There are {len(grouped)} groups of rucksacks.")
    # Now find the sum of the priorities of the common items
    sum_priorities = sum([item_priorities[i] for i in grouped])
    # Print the result
    print(f"Part 2: The sum of the priorities of the common items is {sum_priorities}.")
    return grouped

if __name__ == "__main__":
    input_data = part1()
    part2(input_data)