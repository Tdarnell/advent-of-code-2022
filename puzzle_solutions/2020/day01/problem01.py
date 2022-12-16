import numpy as np
# import the data
infile = np.genfromtxt("inputs/2020/day1.txt", dtype=int)
# produce an array of 2020-the input
search_arr = (infile-2020)*-1
intersects = np.intersect1d(infile, search_arr)
# product of the intersects
prod = np.prod(intersects)
print("Answer: ", intersects, " which sum to ", np.sum(intersects), " and product of these is ", prod)