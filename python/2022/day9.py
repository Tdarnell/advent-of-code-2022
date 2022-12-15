"""
Day 9: Rope Bridge

This problem involves simulating the physics of a moving body with a tow throughout a grid

the grid will look like this:

....
.TH.
....
s...

where s is the start point, T is the towed tail and H is the head of the towed body.

The tail must always be within 1 space of the head, this includes diagonally

The head may pass through the tail, in this case H covers T and there is no tail visible

The instructions will be a series of moves, each move will be a single character, either L, R, U or D 
The instructions will be followed by a number, which is the number of spaces to move in that direction
"""

import sys

sys.path.append(".")
import utils
import re
import operator

# My test case
# U 1 L 3 R 5 D 2 U 5
# The answer for the head should be:
# (0, 1) + (-3, 0) + (5, 0) + (0, -2) + (0, 5) = (2, 4)
# The tail will move as follows:
# (0, 0) + (-2, 1) + (4, 0) + (1, -1) + (0, 3) = (3, 3)

direction = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}


def instructions(
    input_txt: str = "U 1\nL 3\nR 5\nD 2\nU 5\nL 19\nR 5\nU 1\nU 1\nL 3\nD 5\n",
):
    """
    Read the instructions from the input file

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file

    Returns
    -------
    list
        A list of instructions
    """
    # Now we read the input file line by line and parse the instructions as
    # L, R, U or D followed by a number
    lines = input_txt.split("\n")[0:-1]
    instructions = []
    # Use regex to find the instructions and add them to the list
    # They will be in the form of a tuple, so we need to unpack them
    # And parse the number as an integer
    instructions.extend(re.findall(r"([LRUD]) (\d+)", l)[0] for l in lines)
    instructions = [(i[0], int(i[1])) for i in instructions]
    return instructions


def visualiser(
    head_pos,
    tail_pos,
    head_start=(0, 0),
    tail_start=(0, 0),
    visited_points: set = set("[0, 0]"),
):
    """
    This is a visualiser to show the head and tail positions as the instructions are followed
    it is not part of the solution, but it is useful to see what is happening
    """
    # First lets create a grid with (0, 0) in the center, padded with "." to make it look nice
    # We'll make this 300x300 for now
    grid = [["." for _ in range(500)] for _ in range(500)]
    mid_point = (len(grid[0]) // 2, len(grid) // 2)
    # Translate the head start to be in the middle of the grid
    translation = tuple(map(operator.sub, mid_point, head_start))
    head_start = mid_point
    # Now move all other positions by the translation
    for i, pos in enumerate([head_pos, tail_pos, tail_start]):
        pos = tuple(map(operator.add, pos, translation))
        if i == 0:
            head_pos = pos
        elif i == 1:
            tail_pos = pos
        elif i == 2:
            tail_start = pos
    if len(visited_points) > 0:
        visited_points = [
            tuple(map(operator.add, v, translation)) for v in visited_points
        ]
    # Now get all of the visited tiles and add them to the grid as a "#"
    # These are in a set of strings in the format "[x, y]"
    for tile in visited_points:
        # tile = eval(tile)
        grid[tile[1]][tile[0]] = "#"
    # Now we can add the head and tail to the grid
    grid[tail_start[1]][tail_start[0]] = "S"
    grid[head_start[1]][head_start[0]] = "s"
    grid[tail_pos[1]][tail_pos[0]] = "T"
    grid[head_pos[1]][head_pos[0]] = "H"
    grid.reverse()
    output = "\n".join("".join(row) for row in grid)
    # Save the output to a file
    with open("outputs/2022/day9_part1_finalpos.txt", "w") as f:
        f.write(output)


def should_move_tail(head_pos: tuple, tail_pos: tuple):
    """
    This function does the work to determine if the tail should move
    it returns a boolean

    ------------
    Parameters:
    head_pos: tuple
        The position of the head AFTER the current instruction is applied
    tail_pos: tuple
        The position of the tail BEFORE the current instruction is applied
    """
    difference = tuple(map(operator.sub, head_pos, tail_pos))
    # Check if the head is more than 1 space away from the tail in any direction
    if any(abs(d) > 1 for d in difference):
        # if the difference is ever more than 2, raise an error
        if any(abs(d) > 2 for d in difference):
            raise ValueError(f"The head is more than 2 spaces away from the tail, this should not be possible! Happened at position: {head_pos}, {tail_pos}")
        return True


def move_tail(
    instruction: tuple, previous_instruction: tuple, head_pos: tuple, tail_pos: tuple
):
    """
    This function calculates the new position of the tail, given the current instruction
    and the previous instruction applied to move the head. It returns a tuple of the new
    position of the tail.

    ------------
    Parameters:
    instruction: tuple
        The instuction that has just been applied to the head, in the form (x, y)
    previous_instruction: tuple
        The previous instruction that was applied to the head in the previous step
        in the form (x, y)
    head_pos: tuple
        The position of the head AFTER the current instruction is applied, in the form (x, y)
    tail_pos: tuple
        The position of the tail BEFORE the current instruction is applied, in the form (x, y)

    returns:
        tuple
            The new position of the tail, in the form (x, y)
    """
    # First we need to check if the tail should move
    if not should_move_tail(head_pos, tail_pos):
        return tail_pos
    # If the tail should move, we need to calculate the new position
    # Firstly we need to check if the head is currently diagonal to the tail
    # We can do this by comparing the x and y values of the head and tail
    # If both of these are different, then the head is diagonal to the tail
    # If the head is diagonal to the tail, then we need to move the tail in the same direction as the head
    # As well as the direction of the previous instruction
    if head_pos[0] != tail_pos[0] and head_pos[1] != tail_pos[1]:
        """
        This will be true in examples like this:
        
        .....    .....    .....
        .....    ..H..    ..H..
        ..H.. -> ..... -> ..T..
        .T...    .T...    .....
        .....    .....    .....

        .....    .....    .....
        .....    .....    .....
        ..H.. -> ...H. -> ..TH.
        .T...    .T...    .....
        .....    .....    .....
        
        We need to move the tail diagonally to cach up with the head
        So the tail pos will need to be set to the head pos - 1 or + 1 in the axis of the current instruction
        """
        x = head_pos[0] - instruction[0]
        y = head_pos[1] - instruction[1]
        tail_pos = (x, y)
        return tail_pos
    # if (
    #         (
    #             abs(instruction[0]) != abs(previous_instruction[0])
    #             or abs(instruction[1]) != abs(previous_instruction[1])
    #         )
    #     ):
        # The current instruction is moving in a different direction to the previous instruction
        # Now we need to determine if it is a different axis or just a different direction
        # to do this we sum the current instruction and the previous instruction and check if their abs == 2
        # if (
        #     abs(instruction[0]) + abs(instruction[1])
        #     == abs(previous_instruction[0]) + abs(previous_instruction[1])
        # ):
        #     # The current instruction is moving in the same axis as the previous instruction
        #     # We need to move the tail in the same direction as the head
        #     new_tail_pos = tuple(map(operator.add, tail_pos, instruction))
        #     return new_tail_pos
        # # The current instruction is moving in a different axis to the previous instruction
        # # We need to move the tail in the same direction as the head and the previous instruction
        # sum_pos = tuple(map(operator.add, instruction, previous_instruction))
        # new_tail_pos = tuple(map(operator.add, tail_pos, sum_pos))
        # return new_tail_pos
    # If the head is not diagonal to the tail, then we need to move the tail in the same direction as the head only
    new_tail_pos = tuple(map(operator.add, tail_pos, instruction))
    return new_tail_pos


def part1(
    instructions=instructions(),
    start_head=(0, 0),
    start_tail=(0, 0),
    visualise=False,
    verbose=False,
):
    """
    This function calculates the final position of the head and tail after following the instructions
    """
    head_pos = start_head
    tail_pos = start_tail
    tiles_visited = [start_tail]
    # We will need to store the previous instruction to calculate the new position of the tail
    previous_component = (0, 0)
    for step, instruction in enumerate(instructions):
        if verbose:
            print(
                f"Step ({step+1}/{len(instructions)}): {instruction}, head_start: {head_pos}, tail_start: {tail_pos}"
            )
        # First we need to split the instruction into x and y components from the ("Direction": str, Distance: int) tuple
        components = [direction[instruction[0]]] * instruction[1]
        for i, c in enumerate(components):
            # First we need to move the head
            head_pos = tuple(map(operator.add, head_pos, c))
            # Now we need to move the tail
            tail_pos = move_tail(
                instruction=c,
                previous_instruction=previous_component,
                head_pos=head_pos,
                tail_pos=tail_pos,
            )
            # We need to store the previous component to calculate the new position of the tail in the next step
            if verbose:
                print(
                    f"Step ({step+1}/{len(instructions)}): The previous component is {previous_component}, the current component is {c}"
                )
                print(
                    f"Step ({step+1}/{len(instructions)}): Head has moved to {head_pos}, tail has moved to {tail_pos}"
                )
            previous_component = c
            tiles_visited.append(tail_pos)
    return head_pos, tail_pos, tiles_visited


if __name__ == "__main__":
    # Run a test case on the instructions
    # print(moving_body())
    # head_pos, tail_pos, unique_tiles_visited = part1(verbose=True)
    with open(utils.get_input(9, 2022), "r") as f:
        input_data = f.read()
        instr = instructions(input_data)
        # Print the maximum of instructions col 1
        maximum = max([i[1] for i in instr])
        print(
            f"Maximum number of moves: {maximum}, length of instructions: {len(instr)}"
        )
        head_pos, tail_pos, unique_tiles_visited = part1(
            instructions=instr, visualise=False, verbose=True
        )
        print(f"Part 1: {len(set(unique_tiles_visited))} unique tiles visited")
        print(f"Part 1: The final position of the head is {head_pos}, tail is {tail_pos}")
