import sys

sys.path.insert(0, ".")
import utils


def loop_left(grid_row, start_col=0):
    # This will loop through the grid from left to right, optionally from a given index
    # and return the number of trees visible
    # where the grid is a list of integers specifying the tree height
    # with 0 being the smallest and 9 being the tallest
    grid_row = grid_row.copy()
    max_seen = grid_row[start_col]
    # Set all of the trees that are before the start_col to None
    grid_row[:start_col] = [None] * start_col
    # Loop from left to right
    for i, tree in enumerate(grid_row):
        if i <= start_col:
            continue
        if tree > max_seen:
            max_seen = tree
        elif i != start_col:
            grid_row[i] = None
    return grid_row


def loop_right(grid_row, start_col=0):
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
    left_row = loop_left(grid_row, start_col=start_col)
    return left_row[::-1]


def create_rows(grid_text):
    # This will create a list of lists of the grid rows
    lines = grid_text.splitlines()
    rows = []
    for line in lines:
        rows.append([int(x) for x in line])
    return rows


def create_columns(rows: list):
    # This will create a list of lists of the grid columns
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
    # This will return the answer to part 1
    # of the puzzle
    # Read the input file
    with open(input_file) as f:
        text = f.read()
        rows = create_rows(text)
        columns = create_columns(rows)
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
        # Now we transpose our visible columns again using the get_columns function
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
    columns = columns[start_col]
    left_row = loop_left(row, start_col=start_col)
    right_row = loop_right(row, start_col=start_col)
    left_col = loop_left(columns, start_col=start_row)
    right_col = loop_right(columns, start_col=start_row)
    score = []
    for arr in [left_row, right_row, left_col, right_col]:
        score.append(sum(x is not None for x in arr))
    return score[0] * score[1] * score[2] * score[3]

if __name__ == "__main__":
    visible_trees, rows, columns = part1(utils.get_input(8, 2022))
    # save the visible trees to a file
    with open("outputs/2022/day8_part1_visible_trees.txt", "w") as f:
        for row in visible_trees:
            f.write("".join([str(x) if x is not None else "." for x in row]) + "\n")
    # Now we need to find the best place to build a house
    score = get_scenic_score(rows, columns, 10, 10)
    print(f"Part 2: The best place to build a house is at 10, 10 with a score of {score}")