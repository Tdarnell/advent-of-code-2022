import sys
sys.path.insert(0, ".")
import utils

def parse_grid(text):
    # This will parse the grid from the text
    # and return a list of lists of integers
    # where the grid is a list of integers specifying the tree height
    # with 0 being the smallest and 9 being the tallest
    grid = []
    for line in text.splitlines():
        grid.append([int(x) for x in line])
    dimensions = len(grid), len(grid[0])
    return grid, dimensions

def scan_grid(grid, direction="left"):
    # This will scan the grid from left to right
    # and return the index of the furthest visible tree
    # where the grid is a list of integers specifying the tree height
    # with 0 being the smallest and 9 being the tallest
    if direction not in ["left", "right", "up", "down"]:
        raise Exception(f"Direction {direction} is not valid.")
    trees_visible = []
    tree_heights_visible = []
    if direction == "left" or direction == "down":
        range_y = range(len(grid))
        range_x = range(len(grid[0]))
    elif direction == "right":
        range_y = range(len(grid))
        range_x = range(len(grid[0]) - 1, -1, -1)
    elif direction == "up":
        range_y = range(len(grid) - 1, -1, -1)
        range_x = range(len(grid[0]))
    # Scan along the grid looping through the y axis first and then the x axis
    max_height = -1
    print(f"Scanning grid from {direction}, range_y: {range_y}, range_x: {range_x}")
    if direction == "left" or direction == "right":
        for i in range_y:
            max_height = -1
            for j in range_x:
                if grid[i][j] <= max_height:
                    if direction == "left":
                        print(f"i: {i}, j: {j}, grid[i][j]: {grid[i][j]}, Max height: {max_height}")
                        trees_visible.append(j)
                    else:
                        print(f"i: {i}, j: {len(grid[i])-j-1}, grid[i][j]: {grid[i][j]}, Max height: {max_height}")
                        trees_visible.append(len(grid[i])-j-1)
                else:
                    max_height = grid[i][j]
                    tree_heights_visible.append(grid[i][j])
    elif direction == "up" or direction == "down":
        for j in range_x:
            max_height = -1
            for i in range_y:
                # print(f"i: {i}, j: {j}, grid[i][j]: {grid[i][j]}, Max height: {max_height}")
                if grid[i][j] <= max_height:
                    if direction == "up":
                        print(f"i: {len(grid)-i-1}, j: {j}, grid[i][j]: {grid[i][j]}, Max height: {max_height}")
                        trees_visible.append(len(grid)-i-1)
                    else:
                        print(f"i: {i}, j: {j}, grid[i][j]: {grid[i][j]}, Max height: {max_height}")
                        trees_visible.append(i)
                else:
                    max_height = grid[i][j]
                    tree_heights_visible.append(grid[i][j])
    # Trees visible should be no longer than the number of rows if we are scanning left to right
    # print(f"Trees visible: {trees_visible}, {len(trees_visible)}")
    return trees_visible, tree_heights_visible

def part1_old(input_file):
    # This will return the answer to part 1
    # of the puzzle
    # Read the input file
    with open(input_file) as f:
        text = f.read()
        grid, dimensions = parse_grid(text)
        trees_visible = 0
        for direction in ["left", "right", "up", "down"]:
            num_trees = len(scan_grid(grid, direction=direction)[1])
            trees_visible += num_trees
            print(f"The number of trees visible from {direction} is {num_trees}")
        print(f"Part 1: The number of trees visible from outside the grid is {trees_visible}")
        
        
# Starting again as I misunderstood the problem
# You can still see taller trees further down the list after one has been hidden

def loop_left(grid_row, start_col=0):
    # This will loop through the grid from left to right, optionally from a given index
    # and return the number of trees visible
    # where the grid is a list of integers specifying the tree height
    # with 0 being the smallest and 9 being the tallest
    grid_row = grid_row.copy()
    max_seen = grid_row[start_col]
    trees_seen = [grid_row[start_col]]
    # print(f"Looping from 0 to {len(grid_row)}, start_col: {start_col}, max_seen: {max_seen}")
    # Set all of the trees that are before the start_col to None
    grid_row[:start_col] = [None] * start_col
    # Loop from left to right
    for i,tree in enumerate(grid_row):
        if i <= start_col:
            continue
        if tree > max_seen:
            # print(f"Taller tree: {tree}, max_seen before: {max_seen}")
            max_seen = tree
            trees_seen.append(tree)
        elif i != start_col:
            grid_row[i] = None
    # print(f"Trees that can be seen: {trees_seen}")
    # print(f"Grid row: {grid_row}")
    return trees_seen, grid_row
    
def loop_right(grid_row, start_col=0):
    # This will loop through the grid from right to left, optionally from a given index
    # To do this we need to reverse the grid row and then loop from left to right
    # and return the number of trees visible
    # If the start_col is not 0 then we need to reverse the grid row and then
    # work out the index of the tree that we are starting from
    if start_col != 0:
        start_col = len(grid_row) - start_col - 1
    grid_row = grid_row[::-1]
    trees_seen, left_row = loop_left(grid_row, start_col=start_col)
    # print(f"Grid row: {grid_row}")
    return trees_seen, left_row[::-1]

def create_rows(grid_text):
    # This will create a list of lists of the grid rows
    lines = grid_text.splitlines()
    rows = []
    for line in lines:
        rows.append([int(x) for x in line])
    return rows

def create_columns(rows: list):
    # This will create a list of lists of the grid columns
    # rows = create_rows(grid_text)
    # if rows is not a list of lists then raise an error
    if not isinstance(rows, list):
        raise TypeError("rows must be a list")
    if len(rows) == 0:
        raise ValueError("rows must not be empty")
    if not isinstance(rows[0], list):
        raise TypeError("rows must be a list of lists")
    # We now need to iterate through the rows and create a list of columns
    dims = (len(rows), len(rows[0]))
    print(dims)
    # columns = [rows[rw][col] for rw,col in zip(range(dims[1]), range(dims[0]))]
    columns = []
    for col in range(dims[0]):
        columns.append([rows[rw][col] for rw in range(dims[1])])
    # for i in range(dims[0]):
    #     for j in range(dims[1]):
    #         print(f"i: {i}, j: {j}, rows[i][j]: {rows[i][j]}")
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
            trees_seen_l, grid_row_l = loop_left(r)
            trees_seen_r, grid_row_r = loop_right(r)
            visible_rows.append([x if x is not None else y for x,y in zip(grid_row_l, grid_row_r)])
        visible_columns = []
        for c in columns:
            trees_seen_l, grid_row_l = loop_left(c)
            trees_seen_r, grid_row_r = loop_right(c)
            visible_columns.append([x if x is not None else y for x,y in zip(grid_row_l, grid_row_r)])
        # Now we transpose our visible columns again using the get_columns function
        visible_grid = []
        transposed_columns = create_columns(visible_columns)
        for i,row in enumerate(visible_rows):
            visible_grid.append([x if x is not None else y for x,y in zip(row, transposed_columns[i])])
        print(visible_grid)
        # now count the number of trees that are not None
        trees = sum(sum(x is not None for x in row) for row in visible_grid)
        print(f"Part 1: The number of trees visible from outside the grid is {trees}")
        return visible_grid
            
    
if __name__ == "__main__":
    # part1(utils.get_input(8, 2022))
    # test = [1, 8, 3, 4, 5, 6, 7, 8, 9, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # trees_seen_l, grid_row_l = loop_left(test, start_col=4)
    # trees_seen_r, grid_row_r = loop_right(test, start_col=4)
    # # print(grid_row_l, grid_row_r)
    # # combine the grid rows
    # combined_grid_row = [x if x is not None else y for x,y in zip(grid_row_l, grid_row_r)]
    # print(combined_grid_row)
    # trees_seen_l, grid_row_l = loop_left(test)
    # trees_seen_r, grid_row_r = loop_right(test)
    # combined_grid_row = [x if x is not None else y for x,y in zip(grid_row_l, grid_row_r)]
    # print(combined_grid_row)
    # trees_seen_up, grid_row_up = loop_left(create_columns([test] * 19)[0])
    # trees_seen_down, grid_row_down = loop_right(create_columns([test] * 19)[0])
    # combined_grid_ud = [x if x is not None else y for x,y in zip(grid_row_up, grid_row_down)]
    # print(combined_grid_ud)
    
    # with open(utils.get_input(8, 2022)) as f:
    #     text = f.read()
    #     columns = create_columns(text)
    #     print(columns[0])
    visible_trees = part1(utils.get_input(8, 2022))
    # save the visible trees to a file
    with open("outputs/2022/day8_part1_visible_trees.txt", "w") as f:
        for row in visible_trees:
            f.write("".join([str(x) if x is not None else "." for x in row]) + "\n")
    
    