import re
# Import the data as a list
infile = open("inputs/2020/day4.txt", 'r') 
Lines = [line.strip() for line in infile.readlines()] 

# Init variables
passport_data = {}
database = []
invalid = 0
valid = 0

# Structure and populate the database
# byr (Birth Year)
# iyr (Issue Year)
# eyr (Expiration Year)
# hgt (Height)
# hcl (Hair Color)
# ecl (Eye Color)
# pid (Passport ID)
# cid (Country ID)
fields = {
    "byr":(1920, 2002),
    "iyr":(2010, 2020),
    "eyr":(2020, 2030),
    "hgt":{"cm":[150, 193], "in":[59, 76]},
    "hcl":"^#[a-f0-9]{6}$",
    "ecl":['amb','blu','brn','gry','grn','hzl','oth'],
    "pid":"^[0-9]{9}$"
    } #, "cid"} - We are excluding this one for the purpose of the question, naughty elf!

def validate(inp: dict):
    valid = True
    for check in fields.keys():
        if isinstance(fields[check], list):
            # instance of list means it's checking the ecl
            valid = str(inp[check]) in fields[check] 
        elif isinstance(fields[check], tuple):
            # Check integer limits
            valid = min(fields[check]) <= int(inp[check]) <= max(fields[check])
        elif isinstance(fields[check], dict):
            # Check cm/in
            if str(inp[check])[-2:] == "cm":
                valid = min(fields[check]["cm"]) <= int(str(inp[check]).replace("cm", "")) <= max(fields[check]["cm"])
            elif str(inp[check])[-2:] == "in":
                valid = min(fields[check]["in"]) <= int(str(inp[check]).replace("in", "")) <= max(fields[check]["in"])
            else:
                valid = False
        elif isinstance(fields[check], str):
            regex = re.compile(fields[check])
            match = regex.match(inp[check])
            valid = (match != None)
            # Regex comparison
        else:
            # Missed something, throw an error (this could be made into a debug statement)
            valid = False
            print("Error")
        if not valid:
            break
    return valid
        
        

for line in Lines:
    if line != '':
        a = [l.split(':') for l in line.split(' ')]
        for item in a:
            passport_data[item[0]] = item[1]
    if line == '' or ((line == Lines[-1]) and (line != '')):
        if fields.keys() <= passport_data.keys() and validate(passport_data):
            valid+=1
        else:
            invalid+=1
        database.append(passport_data.copy())
        passport_data.clear()

print("Valid passports: ", valid, "\nInvalid passports: ", invalid, "\nTotal passports: ", valid + invalid, "\nTotal database size: ", len(database))