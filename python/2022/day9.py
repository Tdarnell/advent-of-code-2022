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

def instructions(input_txt: str = "U 1\nL 3\nR 5\nD 2\nU 5\n"):
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
    lines = input_txt.split('\n')[0:-1]
    instructions = []
    # Use regex to find the instructions and add them to the list
    # They will be in the form of a tuple, so we need to unpack them
    # And parse the number as an integer
    instructions.extend(re.findall(r"([LRUD]) (\d+)", l)[0] for l in lines)
    instructions = [(i[0], int(i[1])) for i in instructions]
    return instructions

def visualiser(head_pos, tail_pos, head_start = (0, 0), tail_start = (0, 0), visited_points: set = set("[0, 0]")):
    """
    This is a visualiser to show the head and tail positions as the instructions are followed
    it is not part of the solution, but it is useful to see what is happening
    """
    # First lets create a grid with (0, 0) in the center, padded with "." to make it look nice
    # We'll make this 300x300 for now
    grid = [["." for _ in range(500)] for _ in range(500)]
    mid_point = (len(grid[0]) // 2, len(grid) // 2)
    visited_points = [eval(v) for v in visited_points]
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
        visited_points = [tuple(map(operator.add, v, translation)) for v in visited_points]
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

def moving_tow(instructions = instructions(), start_head = (0, 0), start_tail = (0, 0), visualise = False, verbose = False):
    direction = {"L": (-1, 0), "R": (1, 0), "U": (0, 1), "D": (0, -1)}
    head_pos = start_head
    tail_pos = list(start_tail)
    unique_tiles = set()
    unique_tiles.add(str(tail_pos))
    previous_move = (0, 0)
    for step,ins in enumerate(instructions):
        if verbose:
            print(f"Step ({step+1}/{len(instructions)}): {ins}")
        previous_axis = [i for i in range(len(previous_move)) if previous_move[i] != 0]
        for i, d in enumerate([direction[ins[0]]] * ins[1]):
            # The head will move in the direction of the instruction by summing this move with the head position
            _head_pos = (head_pos[0] + d[0], head_pos[1] + d[1])
            if verbose:
                print(f"Move {i+1}: {d}, head: {head_pos}, tail: {tail_pos}, previous move: {previous_move}, previous axis: {previous_axis}")
                print(f"Head moved to {_head_pos}")
            # The tail will only move if the head is now > 1 space away from the tail in any direction
            difference = tuple(map(operator.sub, _head_pos, tail_pos))
            # if any of the differences are not 0 or 1 or -1, then the head has moved more than 1 space away from the tail
            if any(difference[i] not in [-1, 0, 1] for i in range(len(difference))):
            # print(f"Difference between head and tail: {difference}")
            # print(f"Difference between head and tail: {abs(_head_pos[0]) - abs(tail_pos[0])}, {abs(_head_pos[1]) - abs(tail_pos[1])}")
            # if abs(abs(_head_pos[0]) - abs(tail_pos[0])) > 1 or abs(abs(_head_pos[1]) - abs(tail_pos[1])) > 1:
                # If the head has moved in a different axis to the previous move, the tail will move in the previous axis by 1
                # Otherwise if the head has moved in the same axis as the previous move, the tail will move in the same axis by
                # The head move
                this_axis = [i for i in range(len(d)) if d[i] != 0]
                # previous_axis = [i for i in range(len(previous_move)) if previous_move[i] != 0]
                if len(this_axis) == 0 or len(previous_axis) == 0:
                    # The head did not move in any axis, so we can't move the tail
                    pass
                else:
                    if this_axis[0] != previous_axis[0]:
                        # The head has moved in a different axis to the previous move
                        # So we need to move the tail in the previous axis by 1 in the
                        # direction of the previous move
                        if previous_move[previous_axis[0]] > 0:
                            tail_pos[previous_axis[0]] = tail_pos[previous_axis[0]] + 1
                        else:
                            tail_pos[previous_axis[0]] = tail_pos[previous_axis[0]] - 1
                        # now we set the previous axis to the current axis so that the next move will not move the tail
                        # in the previous axis again
                        previous_axis = this_axis
                    # We now need to also move the tail in the same axis as the head move
                    # by the number of spaces the head has moved
                    tail_pos = [tail_pos[0] + d[0], tail_pos[1] + d[1]]
                    unique_tiles.add(str(tail_pos))
                if verbose:
                    print(f"This axis: {this_axis}, previous axis: {previous_axis}")
                    print(f"tail_pos: {tail_pos}")
                    print(f"d: {d}")
                    print(f"Tail moved to {tail_pos}")
            head_pos = _head_pos
        previous_move = (d[0], d[1])
    if visualise:
        visualiser(head_start=start_head, tail_start=start_tail, head_pos=head_pos, tail_pos=tail_pos, visited_points=unique_tiles)
    print(f"Part 1: The final position of the moving body is {head_pos}, it's tail is at {tail_pos} and the tail has visited {len(unique_tiles)} unique tiles")
    return head_pos, tail_pos, len(unique_tiles)
    
    
if __name__ == "__main__":
    # Run a test case on the instructions
    # print(moving_body())
    # head_pos, tail_pos, unique_tiles_visited = moving_tow(visualise=False)
    with open(utils.get_input(9, 2022), "r") as f:
        input_data = f.read()
        instr = instructions(input_data)
        head_pos, tail_pos, unique_tiles_visited = moving_tow(instructions=instr, visualise=True)
