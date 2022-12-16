import re
import numpy as np

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

print("Bags inside the shiny gold bag: ", bag_dict['shiny gold'])

def returnSubBagsCount(bag_list: dict):
    sub_bags = 0
    for (bag,num) in bag_list.items():
        if bag in bag_dict.keys():
            sub_bags += (num * returnSubBagsCount(bag_dict[bag])) + num
        else:  
            # If it is not in the dict then there are no sub bags, count just the number of those bags and return
            sub_bags += num
    return sub_bags

count = returnSubBagsCount(bag_dict['shiny gold']) 
        

print("Number of bags in a shiny gold bag: ", count)
