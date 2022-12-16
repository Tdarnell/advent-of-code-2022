import numpy as np
infile = np.genfromtxt("inputs/2020/day3.txt", dtype=str, delimiter='', comments='%')
# This assumes all rows have the same number of columns
grid = np.array([[n for n in x] for x in infile])
x=0
y=0
answers=[]
while y < np.size(infile):
    if x > 30:
        x = x - 31
    print(x)
    answers.append(grid[y,x])
    x+=3
    y+=1
print(answers.count('#'))