"""
Day 6: Tuning Trouble
"""

from pathlib import Path

input_file = Path("inputs/2022/day6.txt")
if not input_file.exists():
    print(
        f"Input file {input_file} does not exist, please create it in the inputs folder before running this script."
    )
    exit()

def detect_signal(input_data, byte_size=4):
    # For each character in the input data, check if it is has 3 different characters before it
    markers = []
    for i in range(byte_size,len(input_data) + 1, 1):
        if len(set(input_data[i - byte_size : i])) == byte_size:
            markers.append(i)
    return markers


# Part 1
# Split the data by start-of-packet markers, where four characters are all different
def part1(input_file=input_file):
    """
    This function splits the data by start-of-packet markers.

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # Open the input file
    with open(input_file, "r") as f:
        # Read the input file
        input_data = f.read()
        print(len(input_data))
        markers = detect_signal(input_data)
        print(f"Part 1: There are {len(markers)} start-of-packet markers.")
        print(f"Part 1: The first start-of-packet marker is at character {markers[0]}.")
        return input_data

# Part 2
def part2(input_data=None, input_file=input_file):
    """
    This function splits the data by start-of-packet markers.

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
    # Split the data by start-of-packet markers
    markers = detect_signal(input_data, byte_size=14)
    print(f"Part 2: There are {len(markers)} start-of-message markers.")
    print(f"Part 2: The first start-of-message marker is at character {markers[0]}.")

if __name__ == "__main__":
    input_data = part1()
    part2(input_data=input_data)
