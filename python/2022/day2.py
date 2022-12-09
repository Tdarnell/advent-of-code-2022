"""
Day 2: Rock Paper Scissors

"The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--"

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors.

The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) 
plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).
"""

from pathlib import Path

points = {
    "X": 1,  # Rock
    "Y": 2,  # Paper
    "Z": 3,  # Scissors
    "A": 1,  # Rock
    "B": 2,  # Paper
    "C": 3,  # Scissors
    "lose": 0,  # Lose
    "draw": 3,  # Draw
    "win": 6,  # Win
}

input_file = Path("inputs/2022/day2.txt")
if not input_file.exists():
    print(
        f"Input file {input_file} does not exist, please create it in the inputs folder before running this script."
    )
    exit()

# Part 1
# What would your total score be if everything goes exactly according to your strategy guide (input)?
def part1(input_file=input_file):
    """
    This function calculates the total score for following the strategy guide.

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # Open the input file
    with open(input_file, "r") as f:
        # Read the input file
        input_data = f.read()
        # Split the input data into a list of tuples
        input_data = [i.split(" ") for i in input_data.split("\n")]
        # lets work out if we win, lose or draw, then add the points for the shape we played
        # If we play the same shape as our opponent, we draw
        # If we play a shape that beats our opponent, we win
        # If we play a shape that loses to our opponent, we lose
        # The easiest way to do this is using the points values
        # If we play the same shape as our opponent, we get the same points
        # If we play a shape that is +1 or -2 from our opponent, we win
        # If we play a shape that is +2 or -1 from our opponent, we lose
        results = []
        for i in input_data:
            if points[i[0]] == points[i[1]]:
                results.append(points[i[1]] + points["draw"])
            elif points[i[0]] + 1 == points[i[1]] or points[i[0]] - 2 == points[i[1]]:
                results.append(points[i[1]] + points["win"])
            elif points[i[0]] + 2 == points[i[1]] or points[i[0]] - 1 == points[i[1]]:
                results.append(points[i[1]] + points["lose"])
        # Print the result
        print(f"Part 1: The total score is {sum(results)}")
        return input_data


# Part 2
# Now we have been told that X actually means lose, Y means draw, and Z means win.
# Problem is to figure out which shape we should play in response to each shape our opponent plays.
# Then we need to calculate the total score for following our new strategy. We will use the same function as part 1.
def part2(input_data=None):
    """
    This function calculates the total score for following the new strategy.

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # If we have not already run part 1, run it now
    if not input_data:
        input_data = part1()
    # Our play will always be their shapes value + 1 (up to a maximum of 3, then back to 1)
    # So we can use our points dictionary to work out what we should play
    # We can also use the points dictionary to work out what we should play in response to each shape our opponent plays
    new_points = {
        "X": points["lose"],  # lose
        "Y": points["draw"],  # draw
        "Z": points["win"],  # win
        "A": 1,  # Rock
        "B": 2,  # Paper
        "C": 3,  # Scissors
    }
    # if column 2 is X, our points are 0 + their points - 1 (if their points are 1, we play 3)
    # if column 2 is Y, our points are 3 + their points (if their points are 1, we play 3)
    # if column 2 is Z, our points are 6 + their points + 1 (if their points are 1, we play 3)
    result = []
    for a in input_data:
        if new_points[a[1]] == 0:  # lose
            result.append(
                new_points[a[1]]
                + (new_points[a[0]] - 1 if new_points[a[0]] - 1 >= 1 else 3)
            )
        elif new_points[a[1]] == 3:  # draw
            result.append(new_points[a[1]] + new_points[a[0]])
        elif new_points[a[1]] == 6:  # win
            result.append(
                new_points[a[1]]
                + (new_points[a[0]] + 1 if new_points[a[0]] + 1 <= 3 else 1)
            )
    # Print the result
    print(f"Part 2: The total score is {sum(result)}")


if __name__ == "__main__":
    input_data = part1()
    part2(input_data)
