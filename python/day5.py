"""
Day 5: Supply Stacks
"""

from pathlib import Path

input_file = Path(__file__).parent.joinpath("inputs/day5.txt")
if not input_file.exists():
    print(
        f"Input file {input_file} does not exist, please create it in the inputs folder before running this script."
    )
    exit()

def crate_mover(stacks: dict, instructions: list, part=1):
    # we need to loop through the instructions and move the crates
    # where instructions are in the format [move x many, from key, to key]
    moved_stacks = stacks.copy()
    for instruction in instructions:
        # If instruction is not a list of 3 items, skip it and print a warning
        if len(instruction) != 3:
            print(f"Warning: {instruction} is not a valid instruction, skipping.")
            continue
        # First we need to get the crates to move
        crates_to_move = moved_stacks[instruction[1]][-int(instruction[0]) :]
        if part == 1:
            crates_to_move.reverse()
        # Now we need to remove the crates from the original location
        moved_stacks[instruction[1]] = moved_stacks[instruction[1]][:-int(instruction[0])]
        # Now we need to add the crates to the new location
        moved_stacks[instruction[2]] = moved_stacks[instruction[2]] + crates_to_move
    return moved_stacks

# Part 1
def part1(input_file=input_file):
    """
    This function parses the input file and follows the instructions to find where each box ends up.
    """
    # Open the input file
    with open(input_file, "r") as f:
        input_data = f.read()
        # First we need to split the input data into a list of instructions and the crate locations
        input_data = input_data.split("\n\n")
        # the first section is the crate locations
        stacks = input_data[0]
        # The crates are formatted [I] [V] [X] [L] [C] [D] [M] ect.
        # With a final line of      1   2   3   4   5   6   7  ect.
        # We need to split the crates into a list of lists
        # lets get the last line of the crates and count how many characters it has
        contents = list(stacks.split("\n"))
        stacks = {i: [] for i in contents[-1].replace(" ", "")}
        contents.reverse()
        # locate the index of each crates key in the first line of the contents
        column_indexes = {i: contents[0].index(i) for i in stacks.keys()}
        # Now we can loop through the contents and add to the crates dict
        for line in contents[1:]:
            for key, value in stacks.items():
                crate = line[column_indexes[key]]
                if crate != " ":
                    value.append(crate)
                    stacks[key] = value
        # Now we have our initial crate locations, lets get the instructions
        instructions = [
            i.replace("move ", "")
            .replace(" from ", ",")
            .replace(" to ", ",")
            .replace(" ", "")
            .split(",")
            for i in input_data[1].splitlines()
        ]
        rearranged_stacks = crate_mover(stacks, instructions)
        # Now we need to find out which crates are on the top of each stack
        top_crates = []
        for key, value in rearranged_stacks.items():
            top_crates.append(value[-1])
        top_crates = "".join(top_crates)
        print(f"Part 1: The top crates are {top_crates}")
        return stacks, instructions

# Part 2
def part2(stacks=None, instructions=None, input_file=input_file):
    if stacks is None or instructions is None:
        stacks, instructions = part1(input_file)
    # Now we need to run the crate mover again, but this time we do not reverse the crates during movement
    rearranged_stacks = crate_mover(stacks, instructions, part=2)
    # Now we need to find out which crates are on the top of each stack
    top_crates = []
    for key, value in rearranged_stacks.items():
        if len(value) > 0:
            top_crates.append(value[-1])
    top_crates = "".join(top_crates)
    print(f"Part 2: The top crates are {top_crates}")

if __name__ == "__main__":
    stacks, instructions = part1()
    part2(stacks, instructions)
    
