import re

# Import the data as a list
infile = open("inputs/2020/day7.txt", 'r') 
Lines = [line.strip() for line in infile.readlines()] 

bag_dict = {}

for l in Lines:
    tmp = [a.strip() for a in l.replace('bags','').replace('bag', '').replace('contain', ',').replace('.', '').split(',')]
    bags = {}
    for bag in tmp[1:]:
        num = re.search(r'\d+', bag)
        if num != None:
            bags[re.sub(r'[^A-Za-z ]+', '', bag).strip().lower()] = int(num.group())
    if len(bags.values()) > 0:
        bag_dict[tmp[0].lower()] = bags


filtered_bags = []
bag_list = list(bag_dict.keys())

for bag,sub_bags in bag_dict.items():
    to_check = list(sub_bags.keys())
    while len(to_check) > 0:
        if 'shiny gold' in to_check:
            filtered_bags.append(bag)
            to_check = []
            break
        to_add = []
        for b in to_check:
            to_check.remove(b)
            if b in bag_list:
                for a in bag_dict[b].keys():
                    to_add.append(a)
        for item in list(set(to_add)):
            if item not in to_check:
                to_check.append(item)

filtered_bags = list(set(filtered_bags))
print(filtered_bags)

print("Bags that can contain 'shiny gold' at some point: ", len(filtered_bags))
