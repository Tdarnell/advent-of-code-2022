"""
Day 7: No Space Left On Device

This challenge is a work in progress, I found it quite hard! though I think I may be over thinking it by trying to create a file path system...
"""

import re
import sys
sys.path.insert(0, ".")
import utils

def pathwalker(filetree: {}, cwd: str = "/"):
    """
    This function will walk through the filetree and return the cwd dictionary.
    """
    if cwd == "/":
        return filetree
    working_tree = {}
    split_path = list(filter(None, cwd[1:-1].split("/")))
    # Walk the path to the current directory
    for i in range(len(split_path)):
        # Get the path by recursively opening dictionaries in the filetree
        if i == 0:
            if split_path[i] not in filetree:
                print(f"Searched for {split_path[i]} in {filetree}")
                raise Exception(f"Path {cwd} does not exist.")    
            working_tree = filetree[split_path[i]]
        else:
            if split_path[i] not in working_tree:
                print(f"Searched for {split_path[i]} in {working_tree}")
                raise Exception(f"Path {cwd} does not exist.")
            working_tree = working_tree[split_path[i]]
    return working_tree


def savepath(filetree: {}, working_tree: {}, cwd: str = "/"):
    """
    This function will save the working_tree to the filetree at the cwd.
    """
    split_path = list(filter(None, cwd[1:-1].split("/")))
    reversed_path = split_path.copy()
    reversed_path.reverse()
    # We now need to work out what the master dictionary is for the current working directory
    # Walk the path to the current directory
    if len(split_path) == 0:
        filetree = working_tree
        return filetree
    parent_dicts = []
    parent_path = {}
    # print(f"Split path: {split_path}")
    for i,path in enumerate(split_path):
        # print(f"Working on {i}: {path}")
        if len(split_path) == 1:
            filetree[path] = working_tree
            # print(f"Only one path, so filetree is now {filetree}")
            return filetree
        if i == 0:
            parent_dicts.append({path: filetree[path]})
            parent_path = filetree[path]
            # print(f"i == 0, so parent_dicts is now {parent_dicts}")
        elif i < len(split_path) - 1:
            # print(f"parent_dicts[i-1][split_path[i-1]]: {parent_dicts[i-1][split_path[i-1]][split_path[i-1]]}")
            # parent_dicts.append({path: parent_dicts[i-1][split_path[i-1]][split_path[i-1]][path]})
            # print(f"split_path[i-1]: {split_path[i-1]}, path: {path}")
            # parent_path = parent_dicts[i-1][split_path[i-1]][split_path[i-1]][path]
            key, value = (path, parent_path[split_path[i-1]][path])
            parent_key, parent_value = list(parent_dicts[i-1].items())[0]
            print(key, value, parent_key, parent_value)
            exit()
            # print(f"i < len(split_path) - 1, so parent_dicts is now {parent_dicts}")
        elif i == len(split_path) - 1:
            parent_path = {path: working_tree}
            parent_dicts.append(parent_path)
            # print(f"i == len(split_path) - 1, so parent_dicts is now {parent_dicts}")
    # print(f"Parent dicts: {parent_dicts}")
    # Now work backwards through the parent_dicts and update the dictionaries
    parent_dicts.reverse()
    print(f"Parent dicts: {parent_dicts}\n\n")
    print(f"Split path: {split_path}\n\n")
    for i,d in enumerate(parent_dicts):
        # print(f"Working on {i}: {d}")
        if i < len(parent_dicts) - 1:
            # We are in the newly listed directory, lets add it's contents to the next parent
            key = list(d.keys())[0]
            # update the parent with the new directory
            # parent_dicts[i+1][split_path[i+1]][key] = d[key]
            # Update the parent dict value with the new directory listing
            key, value = list(d.items())[0]
            parent_key, parent_value = list(parent_dicts[i+1].items())[0]
            parent_dicts[i+1][parent_key].update({key: value})
            print(key, value, parent_key, parent_value)
            print(parent_dicts[i+1])
            # exit()
            # print(f"Updated {parent_dicts[i+1].keys()} with {d[key]}")
        # elif i < len(parent_dicts) - 1:
        #     print(parent_dicts[i])
        #     # print(f"Updating {parent_dicts[i-1]} with {parent_dicts[i]}")
        #     parent_dicts[i+1] = {**parent_dicts[i+1], **parent_dicts[i]}
        elif i == len(parent_dicts) - 1:
            # print(parent_dicts[i])
            # We should be back at the root, so lets update the filetree
            # print(f"Updating {filetree} with {parent_dicts[i]} at {split_path[0]}")
            filetree.update({split_path[0]: parent_dicts[i]})
    # print(f"Filetree: {filetree}")
    return filetree
    # for i,p in enumerate(reversed_path):
    #         if i == 0:
    #             # This is our working tree, so we can skip it for step 1
    #             parent_path[p] = working_tree
    #             continue
    #         else:
                
            # Recursively walk the path to the current directory and save changes to the filetree
            # parent_path_ = pathwalker(filetree, cwd="/" + "/".join(split_path) + "/")
            # parent_path = {p: parent_path, **pathwalker(filetree, cwd="/" + "/".join(split_path[:len(reversed_path)-i]) + "/")}
            # print(f"Parent path: {parent_path}\nFiletree: {filetree}\nCWD: {cwd}\nSplit path: {split_path}\np: {p}\n")
            # Update the parent path with the new working tree
            # parent_path = {p: pathwalker(filetree, cwd="/" + "/".join(split_path) + "/")}
            # parent_path = {**parent_path_, **parent_path}
            # print(parent_path)
    # filetree.update(parent_path)
    # print(f"Filetree: {filetree}\nCWD: {cwd}\nSplit path: {split_path}\n")
    # return filetree


# Part 1
def part1(input_file = utils.get_input(7, 2022)):
    """

    Parameters
    ----------
    input_file : Path, optional
        The path to the input file, by default input_file
    """
    # Open the input file
    with open(input_file, "r") as f:
        # Read the input file
        input_data = f.read()
        filetree = {}
        working_tree = {}
        summed_tree = 0
        # Now we read the input file line by line
        # Lines starting with $ are commands, either cd to change directory or ls to list files
        # Lines starting with dir are directories
        # Lines starting with numbers are files, the number being their size
        cwd = "/"
        split_lines = input_data.splitlines()
        # Break this into blocks, using lines "$ ls" as the start of a new block and any "$" lines as the end of a block
        blocks = [list(filter(None, a.splitlines())) for a in re.split(r"\$ ", input_data) if a != ""]
        # blocknames = ['']
        # blocknames.extend([re.findall(r"\$ cd (.*)", b[-1])[0] for b in blocks[:-1]])
        # print(blocknames)
        # Each one of these blocks will contain a list of files and directories in the current directory
        # The end of each block will be a "$ cd" command, which will change the current working directory
        # print(blocks)
        # We are only interested in blocks where the total file size is < 100000, so can ignore the rest
        for i,b in enumerate(blocks):
            if i > 10:
                print(f"Breaking at {i}")
                print(f"\n\nFiletree:\n\n{filetree}")
                break
            if i != 0:
                # Find all items which start with a number and sum them
                files = {f.split(" ")[1]: int(f.split(" ")[0]) for f in b if f[0].isdigit()}
                # We need to add the size of the directories to the total
                dirs = {f.split(" ")[1]: {} for f in b if f[0] == "d"}
                # Check that files and dirs are not empty
                if len(files) > 0 or len(dirs) > 0:    
                    # combine the files and directories into a single dictionary
                    working_tree = {**files, **dirs}
                    filetree.update(savepath(filetree, working_tree, cwd))
                    # Now we need to find the cd command at the end of the block to find the next working directory
            for step in re.findall(r"cd (.*)", b[0]):
                if step.split()[0] == "..":
                    print(f"Step is {i} {step}, moving up a directory to {cwd[:cwd[:-1].rfind('/')+1]}")
                    cwd = cwd[:cwd[:-1].rfind("/")+1]
                elif step == "/":
                    print(f"Step is {i} {step}, moving to root directory")
                    cwd = "/"
                else:
                    print(f"Step is {i} {step}, moving to {cwd + step + '/'}")
                    cwd += step + "/"
        # print(f"Block {i} is {blocknames[i]} and the cwd is {cwd}.\nFiletree is {filetree}")
        # print(filetree)
        #    Now we need to look at the previous cd command to find the current working directory
        #     cwd = re.findall(r"\$ cd (.*)", blocks[i-1][-1])[0]
        #     if cwd in filetree:
        #         filetree[cwd] += block_size
        #     else:
        #         filetree[cwd] = block_size
        #     if block_size < 100000:
        #         summed_tree += block_size
        # # print(filetree)
        # # Filter the filetree to only include directories with a size < 100000
        # filtered_tree = {k:v for k,v in filetree.items() if v < 100000}
        # print(filtered_tree)
        # summed_tree = sum(filtered_tree.values())
        # print(f"Part 1: The sum total of folders sizes <100000 are {summed_tree}")
        
if __name__ == "__main__":
    input_file = utils.get_input(7, 2022)
    part1(input_file=input_file)
    