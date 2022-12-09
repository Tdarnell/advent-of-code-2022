import numpy as np
infile = np.genfromtxt("inputs/2020/day3.txt", dtype=str, delimiter='', comments='%')
# This assumes all rows have the same number of columns
grid = np.array([[n for n in x] for x in infile])
itr=[
    {'x':1, 'y': 1}, 
    {'x':3, 'y': 1}, 
    {'x':5, 'y': 1}, 
    {'x':7, 'y': 1}, 
    {'x':1, 'y': 2}
    ]
answers = []
for i in itr:
    x=0
    y=0
    trees=[]
    while y < np.size(infile):
        if x > 30:
            x = x - 31
        print(x)
        trees.append(grid[y,x])
        x+=i['x']
        y+=i['y']
    answers.append(trees.count('#'))
# Interesting, this hits the np.prod integer overflow for a 64 bit number! I learned something here
print(answers, np.prod(np.array(answers, dtype=np.uint8)))