import collections

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
    freq = collections.Counter(g_combined)
    duplicate_chars = [f for f in freq if freq[f] == len(g)]
    summed+=len(duplicate_chars)

print("Sum of duplicate counts: ", summed)