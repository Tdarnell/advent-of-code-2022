# Import the data as a list
infile = open("inputs/2020/day6.txt", 'r') 
Lines = [line.strip() for line in infile.readlines()] 

groups = {1:[]}

i = 1
for line in Lines:
    if line != '':
        groups[i].append(line)
    elif line == '':
        i+=1
        groups[i] = []

summed = 0
for g in groups.values():
    g_combined = ''.join(g)
    unique_chars = ''.join(set(g_combined))
    summed+=len(unique_chars)

print("Sum of counts: ", summed)