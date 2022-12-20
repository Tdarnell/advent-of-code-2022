import sys

sys.path.append(".")
import utils

test_txt = "Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi"

values = {}
for i in range(26):
    values[chr(97 + i)] = i + 1
for i in range(26):
    values[chr(65 + i)] = i + 1 + 26
values["S"] = 1
values["E"] = 26


def format_input(input_txt: str = test_txt, verbose: bool = False):
    input_txt = input_txt.strip()
    lines = input_txt.splitlines()
    chars = [list(line) for line in lines]
    if verbose:
        print(f"Input formatted into {len(chars)} lines of {len(chars[0])} characters")
        print(chars)
    return chars


def get_position(chars: list = format_input(), char: str = "E", verbose: bool = False):
    for i, row in enumerate(chars):
        if char in row:
            if verbose:
                print(f"Found {char} at {i}, {row.index(char)}")
            return i, row.index(char)
    return None


def get_values(chars: list, pos: tuple, verbose: bool = False):
    # If pos is none return the entire char list converted to values
    # else return the value at pos
    if pos is None:
        if verbose:
            print(f"Converting {chars} to values")
        return [[values[char] for char in row] for row in chars]
    else:
        if verbose:
            print(f"Converting {chars[pos[0]][pos[1]]} to value")
        return values[chars[pos[0]][pos[1]]]


def get_adjacent_values(chars: list, pos: tuple, verbose: bool = False):
    """
    Given a list of lists (chars) and a position (pos) in the list, return the
    adjacent positions in the list. In the case of a position that is on the edge
    of the list, the position will be None.
    If verbose is True, print out the dimensions of the list and the adjacent
    positions to the console.
    """
    # Firstly we need to determine the dimensions of the char list
    # We can then work out which indexes represent the adjacent values
    # for up, down, left and right
    try:
        dims = len(chars), len(chars[0])
    except IndexError:
        print("There is no data in the chars list")
        return None, None, None, None
    if verbose:
        print(f"Dimensions of char list are {dims}")
    if pos[0] == 0:
        if verbose:
            print("Top row")
        up = None
        down = (pos[0] + 1, pos[1])
    elif pos[0] == dims[0] - 1:
        if verbose:
            print("Bottom row")
        up = (pos[0] - 1, pos[1])
        down = None
    else:
        if verbose:
            print("Middle")
        up = (pos[0] - 1, pos[1])
        down = (pos[0] + 1, pos[1])
    if pos[1] == 0:
        if verbose:
            print("Left column")
        left = None
        right = (pos[0], pos[1] + 1)
    elif pos[1] == dims[1] - 1:
        if verbose:
            print("Right column")
        left = (pos[0], pos[1] - 1)
        right = None
    else:
        if verbose:
            print("Middle")
        left = (pos[0], pos[1] - 1)
        right = (pos[0], pos[1] + 1)
    if verbose:
        print(f"Adjacent values are {up}, {down}, {left}, {right}")
    return up, down, left, right


def build_graph(chars: list, verbose: bool = False):
    """
    Given a list of lists (chars) build a graph of the values in the list
    """
    # Firstly we need to determine the dimensions of the char list
    # We can then work out which indexes represent the adjacent values
    # for up, down, left and right
    try:
        dims = len(chars), len(chars[0])
    except IndexError:
        print("There is no data in the chars list")
        return None, None, None, None
    if verbose:
        print(f"Dimensions of char list are {dims}")
    graph = {}
    for i in range(dims[0]):
        for j in range(dims[1]):
            # graph[(i, j)] = get_adjacent_values(chars, (i, j), verbose=verbose)
            graph[(i, j)] = {pos: get_values(chars, pos) for pos in get_adjacent_values(chars, (i, j), verbose=verbose) if pos is not None}
    return graph

# I understand that I need to solve the djikstra algorithm to solve this problem
# I have not yet done this, but I have written the code to build the graph

if __name__ == "__main__":
    chars = format_input(verbose=True)
    pos_E = get_position(verbose=True)
    pos_S = get_position(char="S", verbose=True)
    char_vals = get_values(chars, pos=None, verbose=True)
    print(char_vals)
    u, d, l, r = get_adjacent_values(chars, pos_E, verbose=True)
    u, d, l, r = get_adjacent_values(chars, pos_S, verbose=True)
    graph = build_graph(chars, verbose=True)
    print(f"Graph is {graph}")