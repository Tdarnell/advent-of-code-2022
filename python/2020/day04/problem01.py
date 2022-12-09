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
keys = ("byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid") #, "cid"} - We are excluding this one for the purpose of the question, naughty elf!
for line in Lines:
    if line != '':
        a = [l.split(':') for l in line.split(' ')]
        for item in a:
            passport_data[item[0]] = item[1]
    if line == '' or ((line == Lines[-1]) and (line != '')):
        if set(keys) <= passport_data.keys():
            valid+=1
        else:
            invalid+=1
        database.append(passport_data.copy())
        passport_data.clear()

print("Valid passports: ", valid, "\nInvalid passports: ", invalid, "\nTotal passports: ", valid + invalid, "\nTotal database size: ", len(database))