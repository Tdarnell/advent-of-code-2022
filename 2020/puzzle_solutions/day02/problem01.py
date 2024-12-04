from collections import Counter
infile = open("inputs/2020/day2.txt", 'r') 
# Create an array where [[Start, End, character, password]]
Lines = [line.strip().replace(':', '').replace('-', ' ').split(' ') for line in infile.readlines()] 
invalid = []
for line in Lines:
    min_x = line[0]
    max_x = line[1]
    char = line[2]
    password = line[3]
    letters = Counter(password)
    print(letters)
    if letters[str(char)] < int(min_x) or letters[str(char)] > int(max_x):
        invalid.append([min_x, max_x, char, password])
print('Total: ', len(Lines), 'Valid: ',  len(Lines) - len(invalid), 'Invalid: ', len(invalid))