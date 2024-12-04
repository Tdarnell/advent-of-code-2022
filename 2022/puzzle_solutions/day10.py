import sys

sys.path.append(".")
import utils
import re


def cycle(
    instruction: str = "noop",
    X: int = 1,
    start_cycle: int = 0,
    cursor_pos: int = 1,
    verbose: bool = False,
):
    """
    Runs a cycle of instructions, returning the value of X after the cycle, and the cycle number.

    If the instruction crosses a cycle boundary, cycle_num %% 20, then calculate the signal strength and return it too.
    """
    cycle_num = start_cycle
    cycles = 1 if instruction == "noop" else 2
    signal = None
    CRT = []
    while cycles > 0:
        # print(f"Cycle {cycle_num}, Is 20th cycle? {cycle_num % 20 == 0}")
        cycle_num += 1
        # if the CRT_pos is > 39, then subtract cycle_num - (cycle_num - 39) 
        CRT_pos = cycle_num - (40 * int(cycle_num / 40)) - 1 if cycle_num > 40 else cycle_num - 1
        if verbose:
            if cycle_num - 1 == start_cycle:
                print(f"Start cycle {start_cycle}: begin executing {instruction}")
            print(f"During cycle {cycle_num}: CRT draws pixel in position {CRT_pos}")
            sprite_drawing = ["░░" for _ in range(40)]
            for r in range(cursor_pos - 1, cursor_pos + 2):
                if r < 0:
                    continue
                sprite_drawing[r] = "██"
                sprite_drawing[CRT_pos] = "XX"
            print(f"Sprite position: {''.join(sprite_drawing)}")
            print(f"Cycle {cycle_num}, CRT_pos = {CRT_pos}")
        # If the cycle_num is within +/-1 of the cursor position, then CRT append cycle_num
        if CRT_pos in range(cursor_pos - 1, cursor_pos + 2):
            if verbose:
                print(f"Appending {cycle_num} to CRT as it's within +/-1 of cursor position {cursor_pos}")
            CRT.append(CRT_pos + (40 * int(cycle_num / 40)))
        if cycle_num % 20 == 0:
            # calculate signal strength
            if verbose:
                print(f"Calculating signal strength for cycle {cycle_num} with X = {X}")
            signal = X * cycle_num
        cycles -= 1
        # Use regex to parse the instruction, can be "noop" or "addx <int>"
        # If it's addx, get the value of X
    if instruction != "noop":
        value = int(re.search(r"addx (-?\d+)", instruction).group(1))
        X += value
    return X, cycle_num, signal, CRT


def run_program(
    instructions: list = [
        "addx 15",
        "addx -11",
        "addx 6",
        "addx -3",
        "addx 5",
        "addx -1",
        "addx -8",
        "addx 13",
        "addx 4",
        "noop",
    ],
    X: int = 1,
    start_cycle: int = 0,
    cursor_pos: int = 1,
    verbose: bool = False,
):
    signals = []
    CRT = []
    for inst in instructions:
        X, cycle_num, signal, CRT_ = cycle(
            instruction=inst, X=X, start_cycle=start_cycle, cursor_pos=X, verbose=verbose
        )
        if signal is not None:
            signals.append(signal)
        if len(CRT_) > 0:
            CRT.extend(CRT_)
        start_cycle = cycle_num
    return X, cycle_num, signals, CRT


def draw_CRT(CRT: list):
    # This will draw a 6 x 40 list of "." and "#" characters
    # Then it will populate the list with the values of the CRT - 1
    screen = ["░░" for _ in range(40 * 6)]
    print(len(screen))
    for pos in CRT:
        screen[pos] = "██"
    # print(screen)
    output = ""
    for row in range(6):
        output += "".join(screen[row * 40 : (row + 1) * 40]) + "\n"
    return output


if __name__ == "__main__":
    # Part 1
    input_file = utils.get_input(day=10, year=2022)
    with open(input_file, "r") as f:
        input_data = f.read()
        instructions = input_data.splitlines()
        # print(f"Instructions: {instructions}")
        # If the last line is blank, remove it
        instructions = instructions[:-1] if instructions[-1] == "" else instructions
        x, cycle_num, signals, CRT = run_program(instructions, verbose=True)
        print(f"Part 1: X={x}, cycle={cycle_num}, signals={signals}")
        part_1_wanted_signals = [20, 60, 100, 140, 180, 220]
        part_1_wanted_signals_idx = [int(a / 20) - 1 for a in part_1_wanted_signals]
        print(f"Part 1 wanted signals: {part_1_wanted_signals}")
        part_1_sum_signal = sum([signals[a] for a in part_1_wanted_signals_idx])
        print(f"Part 1: signal strength = {part_1_sum_signal}")
        # Part 2
        CRT_text = draw_CRT(CRT)
        print(f"Part 2: CRT =\n{CRT_text}")
        # Save to file
        with open("outputs/2022/day10_part2_CRT.txt", "wb") as f:
            f.write(CRT_text.encode("utf-8"))