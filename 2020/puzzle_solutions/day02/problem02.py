infile = open("inputs/2020/day2.txt", 'r') 
# Create an array where [[Start, End, character, password]]
Lines = [line.strip().replace(':', '').replace('-', ' ').split(' ') for line in infile.readlines()] 
invalid = []
valid = []
for line in Lines:
    min_x = int(line[0])
    max_x = int(line[1])
    char = str(line[2])
    password = str(line[3])
    char1 = password[min_x-1] == char
    char2 = password[max_x-1] == char
    if char1 != char2:
        valid.append([min_x, max_x, char, password])
    else: 
        invalid.append([min_x, max_x, char, password])
    
print('Total: ', len(Lines), 'Valid: ',  len(valid), 'Invalid: ', len(invalid))