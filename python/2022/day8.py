import sys

sys.path.insert(0, ".")
import utils
import math


def loop_left(grid_row, start_col=0, include_start=True):
    """
    This will loop through the grid from left to right, optionally from a given index
    and return the number of trees visible
    where the grid is a list of integers specifying the tree height
    with 0 being the smallest and 9 being the tallest
    """
    grid_row = grid_row.copy()
    max_seen = grid_row[start_col]
    # Set all of the trees that are before the start_col to None
    # If we are not including the start then we need to set the start to None too
    if not include_start:
        grid_row[start_col] = None
    grid_row[:start_col] = [None] * start_col
    # Loop from left to right
    for i, tree in enumerate(grid_row):
        # If we are before the start_col then continue
        if i <= start_col:
            continue
        # If the tree is taller than the max seen then set the max seen to the tree
        # Note that if we are not including the start then we need to set all of the
        # trees after the new max seen to None
        if tree > max_seen or (tree == max_seen and not include_start):
            if not include_start:
                grid_row[i + 1 :] = [None] * (len(grid_row) - i - 1)
                break
            max_seen = tree
        # If we are not including the start then we need to include trees shorter than the max seen
        # This is because we are starting observing from a height greater than the tree
        elif tree < max_seen and not include_start:
            continue
        # If the tree is shorter than the max seen then set the tree to None, we can't see it
        elif i != start_col:
            grid_row[i] = None
    return grid_row


def loop_right(grid_row, start_col=0, *args, **kwargs):
    """
    This will loop through the grid from right to left, optionally from a given index
    To do this we need to reverse the grid row and then loop from left to right
    and return the number of trees visible
    If the start_col is not 0 then we need to reverse the grid row and then
    work out the index of the tree that we are starting from
    """
    if start_col != 0:
        start_col = len(grid_row) - start_col - 1
    grid_row = grid_row[::-1]
    left_row = loop_left(grid_row, start_col=start_col, *args, **kwargs)
    return left_row[::-1]


def create_rows(grid_text):
    """This will create a list of lists of the grid rows"""
    lines = grid_text.splitlines()
    rows = []
    for line in lines:
        rows.append([int(x) for x in line])
    return rows


def create_columns(rows: list):
    """This will create a list of lists of the grid columns"""
    # if rows is not a list of lists then raise an error
    if not isinstance(rows, list):
        raise TypeError("rows must be a list")
    if len(rows) == 0:
        raise ValueError("rows must not be empty")
    if not isinstance(rows[0], list):
        raise TypeError("rows must be a list of lists")
    # We now need to iterate through the rows and create a list of columns
    dims = (len(rows), len(rows[0]))
    columns = []
    for col in range(dims[0]):
        columns.append([rows[rw][col] for rw in range(dims[1])])
    return columns


def part1(input_file):
    """
    For this part of the puzzle we want to work out how many trees can be seen from outside the grid
    We do this by looping through all of the rows and columns and working out how many trees can be seen
    First from the left and then from the right and then we transpose the columns and do the same again
    """
    # Read the input file
    with open(input_file) as f:
        text = f.read()
        rows = create_rows(text)
        columns = create_columns(rows)
        # Loop through the rows and columns and work out how many trees can be seen
        visible_rows = []
        for r in rows:
            grid_row_l = loop_left(r)
            grid_row_r = loop_right(r)
            visible_rows.append(
                [x if x is not None else y for x, y in zip(grid_row_l, grid_row_r)]
            )
        visible_columns = []
        for c in columns:
            grid_row_l = loop_left(c)
            grid_row_r = loop_right(c)
            visible_columns.append(
                [x if x is not None else y for x, y in zip(grid_row_l, grid_row_r)]
            )
        # Now we transpose our visible columns using the get_columns function
        # We do this so we can combine the rows and columns into a single grid
        # And they are in the same orientation
        visible_grid = []
        transposed_columns = create_columns(visible_columns)
        for i, row in enumerate(visible_rows):
            visible_grid.append(
                [x if x is not None else y for x, y in zip(row, transposed_columns[i])]
            )
        # now count the number of trees that are not None
        trees = sum(sum(x is not None for x in row) for row in visible_grid)
        print(f"Part 1: The number of trees visible from outside the grid is {trees}")
        return visible_grid, rows, columns


def get_scenic_score(rows, columns, start_col, start_row):
    """
    This will return the scenic score for the given row and column
    It does this by looping through the rows and columns and
    working out how many trees can be seen left, right, up and down
    from that given point. It then multiplies these numbers together.
    """
    # get the row and column that we are starting from
    row = rows[start_row]
    column = columns[start_col]
    arrs = []
    # Loop through the row and column and work out how many trees can be seen
    # If we are on an edge then we need to make sure we don't observe past the edge
    if start_col < len(row) - 1:
        left_row = loop_left(row, start_col=start_col, include_start=False)
        arrs.append(left_row)
    if start_col > 0 and start_col < len(row):
        right_row = loop_right(row, start_col=start_col, include_start=False)
        arrs.append(right_row)
    if start_row < len(column):
        left_col = loop_left(column, start_col=start_row, include_start=False)
        arrs.append(left_col)
    if start_row > 0 and start_row < len(column):
        right_col = loop_right(column, start_col=start_row, include_start=False)
        arrs.append(right_col)
    score = []
    for arr in arrs:
        score.append(sum(x is not None for x in arr))
    return math.prod(score), arrs


def part2(rows, columns, visualise=False):
    """
    This puzzle involves looping through all trees within the grid and working out the scenic score
    Where the scenic score is the product of all visible tree heights from that point
    """
    dimensions = (len(rows), len(columns))
    highest_score = 0
    highest_arr = None
    # Loop through the rows and columns and work out the scenic score
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            score, arrs = get_scenic_score(rows, columns, i, j)
            if score > highest_score:
                print(f"Score at {i}, {j} [{rows[i][j]}] is {score}")
                highest_score = score
                highest_index = (i, j)
                highest_arr = arrs
    print(f"Part 2: The highest score is {highest_score} at index {highest_index}")
    return highest_score, highest_index, highest_arr


if __name__ == "__main__":
    visible_trees, rows, columns = part1(utils.get_input(8, 2022))
    # save the visible trees to a file
    with open("outputs/2022/day8_part1_visible_trees.txt", "w") as f:
        for row in visible_trees:
            f.write("".join([str(x) if x is not None else "." for x in row]) + "\n")
    highest_score, highest_index, highest_arr = part2(rows, columns, visualise=True)
    dimensions = (len(rows), len(columns))
    """
    This is section is purely for visualising the highest score for part2 in an ASCII grid
    It is not needed for the puzzle solution, but I like to see the results
    """
    # We are going to create a list of lists, filled with None of the same dimensions as the grid
    # Then we are going to loop through the arrs and add the values to the grid
    # We need to work out which arrs are which, and then add them to the correct index
    if len(highest_arr) != 4:
        print(
            f"The length of highest_arr is {len(highest_arr)}, this means our optimal spot is along an edge"
        )
        print(
            f"Now we need to work out which edge it is on but looking at the indexes of the highest_arr"
        )
        print([[x for x in arr if x is not None] for arr in highest_arr])
        # This should never be the case really... but the logic here would be worth working out if it was
        # For now I will not be doing this as it is not needed for the puzzle
    if len(highest_arr) == 4:
        print(
            f"The length of highest_arr is {len(highest_arr)}, this means our optimal spot is in the middle somewhere"
        )
        # This means we have a left row, right row, left column and right column
        # We need to add the left row to the grid at index 0, the right row to the grid at index 1
        # The left column to the grid at index 2, and the right column to the grid at index 3
        grid = [[None for x in range(dimensions[1])] for y in range(dimensions[0])]
        print(
            f"Using indexes {highest_index} to create a visualisation of the grid at this point"
        )
        row_n = highest_index[0]  # The row number
        col_n = highest_index[1]  # The column number
        print(
            f"The value at this index is rows: {rows[row_n][col_n]}, columns: {columns[col_n][row_n]}"
        )
        # rn is the row number, we will need to use this to access the correct row in the up down columns
        # cn is the column number, we will need to use this to access the correct column in the left right rows
        # We will need to loop through the values in the highest_arrays and add them to the grid at their respective indexes
        for i, arr in enumerate(highest_arr):
            # if i == 1 or i == 3:
            # arr = arr[::-1]
            for j, val in enumerate(arr):
                if i == 0 or i == 1:
                    if val is not None:
                        # print(f"Adding {val} to grid[{j}][{col_n}]")
                        grid[j][col_n] = val
                if i == 2 or i == 3:
                    if val is not None:
                        # print(f"Adding {val} to grid[{row_n}][{j}]")
                        grid[row_n][j] = val
        # Now we need to write the grid to a file
        with open("outputs/2022/day8_part2_visualise.txt", "w") as f:
            for row in grid:
                f.write("".join([str(x) if x is not None else "." for x in row]) + "\n")
