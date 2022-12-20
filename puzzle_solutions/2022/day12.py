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
    pos_value = chars[pos[0]][pos[1]]
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
    adj_values = [up, down, left, right]
    for i, pos in enumerate(adj_values):
        if pos is not None:
            if verbose:
                print(f"Value at {pos} is {chars[pos[0]][pos[1]]}")
            val = chars[pos[0]][pos[1]]
            # If the val is not within +/- 1 of the pos_value, set the pos to None
            if abs(values[val] - values[pos_value]) > 1:
                if verbose:
                    print(f"Value at {pos} is not within +/- 1 of {pos_value}")
                adj_values[i] = None
    return adj_values


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
            graph[(i, j)] = {
                pos: get_values(chars, pos)
                for pos in get_adjacent_values(chars, (i, j), verbose=verbose)
                if pos is not None
            }
    return graph


## Dijkstra's algorithm
# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
# https://www.youtube.com/watch?v=gdmfOwyQlcI
# Excellent Learning material for this: https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Better implementation available: https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar
# Their implementation however depends on a priority queue, for my understanding I will implement it without
# as I am learning this algorithm for the first time.
# Code for this function written with assistance from OpenAI ChatGPT
def dijkstra(graph: list, start: tuple, end: tuple):
    if not isinstance(graph, dict) or not isinstance(start, tuple) or not isinstance(end, tuple):
        raise Exception("Graph must be a dictionary and start and end must be tuples.")
    if start not in graph or end not in graph:
        raise Exception("Start or end node not in graph.")
    # create a dictionary to store the cost (distance) to each node
    # set the cost to infinity for all nodes
    cost_to_node = {node: float("inf") for node in graph}
    # set the cost to the start node to 0
    cost_to_node[start] = 0
    # create a dictionary to store the parent of each node in the shortest path
    parent = {node: None for node in graph}
    # create a set to store the visited nodes
    visited = set()

    # loop until the end node is visited
    while end not in visited:
        # find the node with the smallest distance that has not been visited
        smallest = float("inf")
        current_node = None
        for node, cost in cost_to_node.items():
            if cost < smallest and node not in visited:
                smallest = cost
                current_node = node
        # if there are no unvisited nodes left, we are done
        if current_node is None:
            break
        # mark the current node as visited
        visited.add(current_node)
        # consider all of the current node's neighbors
        for neighbor, cost in graph[current_node].items():
            # calculate the cost to the neighbor through the current node
            new_cost = cost_to_node[current_node] + cost
            # if the new cost is less than the current cost to the neighbor, update the cost and set the current node as the neighbor's parent
            if new_cost < cost_to_node[neighbor]:
                cost_to_node[neighbor] = new_cost
                parent[neighbor] = current_node
    print(f"Cost to node {end} is {cost_to_node[end]}")
    print(f"Parent of node {end} is {parent[end]}")
    # print(cost_to_node)
    # print(f"Visited nodes are {visited}")
    # create a list to store the shortest path
    shortest_path = []
    # set the current node to the end node
    current_node = end
    # loop through the parent dictionary to build the shortest path
    while current_node is not None:
        shortest_path.append(current_node)
        current_node = parent[current_node]
    # reverse the list to get the shortest path in the correct order
    shortest_path.reverse()
    # return the shortest path and the cost
    return shortest_path, cost_to_node[end]


if __name__ == "__main__":
    # chars = format_input(verbose=True)
    # pos_E = get_position(verbose=True)
    # pos_S = get_position(char="S", verbose=True)
    # char_vals = get_values(chars, pos=None, verbose=True)
    # print(char_vals)
    # u, d, l, r = get_adjacent_values(chars, pos_E, verbose=True)
    # u, d, l, r = get_adjacent_values(chars, pos_S, verbose=True)
    # graph = build_graph(chars, verbose=True)
    # graph_values_E = graph[pos_E]
    # print(f"Graph is {graph}, graph_values_E is {graph_values_E}")
    # shortest_path, cost = dijkstra(graph, pos_S, pos_E)
    # print(
    #     f"Shortest path is {shortest_path} with a length of {len(shortest_path) - 1}, it has a cost of {cost}"
    # )
    ## Part 1
    input_data = utils.get_input(year=2022, day=12)
    with open(input_data) as f:
        input_txt = f.read().strip()
        chars = format_input(input_txt=input_txt, verbose=False)
        pos_E = get_position(chars, verbose=False)
        pos_S = get_position(chars, char="S", verbose=False)
        print(f"pos_E is {pos_E}, pos_S is {pos_S}")
        graph = build_graph(chars, verbose=False)
        print(f"Graph of size {len(graph)} built")
        print(f"The graph values for pos_S are {graph[pos_S]} and for pos_E are {graph[pos_E]}")
        shortest_path, cost = dijkstra(graph, start=pos_S, end=pos_E)
        # Worked for the example, but not for the actual input, so I need to debug this in the morning
        # I think the problem is that the start is not (0, 0) as it was in the example
        print(f"Shortest path is {shortest_path} with a cost of {cost}")
        print(f"Part 1: {len(shortest_path) - 1}")
        
        
