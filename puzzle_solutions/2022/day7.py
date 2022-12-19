"""
Day 7: No Space Left On Device

This challenge is a work in progress, I found it quite hard! though I think I may be over thinking it by trying to create a file path system...
"""

import re
import sys

sys.path.insert(0, ".")
import utils


def get_dir(input_str: str = "dir d"):
    """
    This function will take the input string and return the directory name
    """
    # Use regex to get the directory name (everything after "dir ")
    # By using regex, we can handle spaces in the directory name
    return re.search(r"dir (.+)", input_str).group(1)


def get_file(input_str: str = "2557 g"):
    """
    This function will take the input string and return the file name and size
    """
    # Use regex to get the file name and size (format is "size name")
    # By using regex, we can handle spaces in the file name
    groups = re.search(r"(\d+) (.+)", input_str).groups()
    size = int(groups[0])
    name = groups[1]
    return name, size


def get_command(input_str: str = "$ cd a"):
    """
    This function will take the input string and return the command and directory name
    """
    print(input_str)
    # Use regex to get the command and directory name (format is "$ command directory")
    # the directory name is optional
    # By using regex, we can handle spaces in the directory name
    groups = re.search(r"\$ (\w+) ?(.+)?", input_str).groups()
    command = groups[0]
    if command == "cd":
        directory = groups[1]
    elif command == "ls":
        directory = None
    return command, directory


## This function did not get used in the end, but I have left it here for reference
## As I think it is a good example of how to use recursion to build a tree
def treebuilder(
    folders: list = ["/", "/a/", "/a/b/", "/d/"],
) -> dict:
    """
    This function will take a list of folders and return a dictionary of the folder tree
    """
    filetree = {}
    for folder in folders:
        # first we need to split the folders into their components
        components = folder.split("/")
        # remove all '' components
        components = [component for component in components if component != ""]
        # now for each component we need to add it to the filetree as a nested dictionary
        # we need reverse the components so we can add the folders in the correct order
        if len(components) < 1:
            # root folder
            continue
        if len(components) == 1:
            filetree[components[0]] = {}
            continue
        components.reverse()
        _workingtree, cwd = {}, components[-1]
        for c in components[:-1]:                
            _workingtree = {c: _workingtree}
        if filetree == {}:
            filetree = _workingtree
        elif cwd in filetree:
            filetree[cwd].update(_workingtree)
        else:
            filetree[cwd] = _workingtree
    return filetree

def pathmapper(
    input_txt: str = "$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\ndir e\n29116 f\n"
    "2557 g\n62596 h.lst\n$ cd e\n$ ls\n584 i\n$ cd ..\n$ cd ..\n$ cd d\n$ ls\n4060174 j\n8033020 d.log\n"
    "5626152 d.ext\n7214296 k\n",
):
    """
    This function will take the input text and return a dictionary of the paths
    """
    input_txt = input_txt.strip().splitlines()
    foldersizes = {}
    paths = []
    parent, contents = "/", []
    for i, line in enumerate(input_txt):
        # check what operation we are doing on the line
        if "$" in line:
            # This is a command
            command, _directory = get_command(line)
            if command == "cd":
                if len(contents) > 0:
                    # we need to add the contents to the foldersizes
                    paths.append(parent)
                    foldersizes[parent] = contents
                    contents = []
                if _directory == "/":
                    parent = "/"
                elif _directory == "..":
                    parent = "/".join(parent.split("/")[:-2]) + "/"
                else:
                    parent = parent + _directory + "/"
        elif "dir " in line:
            # This is a directory
            _directory = get_dir(line)
            contents.append(parent + _directory + "/")
        else:
            # This is a file with a file size
            _file, _size = get_file(line)
            contents.append(_size)
    paths.append(parent)
    foldersizes[parent] = contents
    for path in paths:
        # now we are going to replace any strings in each foldersize with the contents of that folder
        # we do this in a while loop so we can handle nested folders
        strings = [content for content in foldersizes[path] if isinstance(content, str)]
        while len(strings) > 0:
            for string in strings:
                # get the contents of the string folder and put it in the foldersizes, remove the string
                foldersizes[path].remove(string)
                foldersizes[path].extend(foldersizes[string])
            strings = [content for content in foldersizes[path] if isinstance(content, str)]
    # Now we sum the sizes of each folder and replace the list with the sum
    for path, contents in foldersizes.items():
        foldersizes[path] = sum(contents)
    # now we are going to replace any strings in each foldersize with the contents of that folder
    return foldersizes


if __name__ == "__main__":
    input_file = utils.get_input(7, 2022)
    with open(input_file, "r") as f:
        input_txt = f.read()
        # part 1
        foldersizes = pathmapper(input_txt=input_txt)
        print(f"There are {len(foldersizes)} folders")
        print(f"The largest folder is {max(foldersizes.values())} bytes, it is in {max(foldersizes, key=foldersizes.get)}")
        # Find all of the directories with a total size of at most 100000
        smallfolders = [folder for folder, size in foldersizes.items() if size <= 100000]
        # sum their sizes
        sizes = sum([foldersizes[folder] for folder in smallfolders])
        print(f"There are {len(smallfolders)} folders with a total size of {sizes} bytes")
        # part 2
        # total disk space = 70000000
        # needed space = 30000000
        # total used space = "/" size in the foldersizes, 50822529 in our case
        freespace = 70000000 - max(foldersizes.values())
        # Find the smallest directory that, if deleted, would free up enough space
        neededsize = 30000000 - freespace
        # filter the foldersizes to only include folders that are greater than the needed size
        options = [folder for folder, size in foldersizes.items() if size >= neededsize]
        # sort by size and select the smallest
        options.sort(key=lambda x: foldersizes[x])
        smallest = options[0]
        print(f"The smallest folder that, if deleted, would free up enough space is {smallest} with a size of {foldersizes[smallest]} bytes")
