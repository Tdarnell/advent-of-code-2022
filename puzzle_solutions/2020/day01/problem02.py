import numpy as np
# import the data
infile = np.genfromtxt("inputs/2020/day1.txt", dtype=int)
# produce a sum product array
sum_array1 = np.array([infile + n for n in infile])
# subtract 2020 from all sum products
search_arr = (sum_array1-2020)*-1
# Find the duplicate between the input array and the sum product - 2020
intersects = np.intersect1d(infile, search_arr)
# product of the intersects
prod = np.prod(intersects)
print("Answer: ", intersects, " which sum to ", np.sum(intersects), " and product of these is ", prod)