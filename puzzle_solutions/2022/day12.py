import sys

sys.path.append(".")
import utils

test_txt = "Sabqponm\nabcryxxl\naccszExk\nacctuvwj\nabdefghi"

values = {
}
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

def next_move(chars: list, pos_E: tuple, pos_S: tuple, verbose: bool = False ):
    pass

if __name__ == "__main__":
    chars = format_input(verbose=True)
    pos_E = get_position(verbose=True)
    pos_S = get_position(char="S", verbose=True)
    char_vals = get_values(chars, pos=None, verbose=True)
    print(char_vals)
    # print(values)