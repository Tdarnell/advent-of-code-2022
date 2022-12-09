import math

# Import the data as a list
infile = open("inputs/2020/day5.txt", 'r') 
Lines = [line.strip() for line in infile.readlines()] 

seat_ids = []

for seat in Lines:
    row = list(range(0, 128, 1))
    col = list(range(0, 8, 1))

    for char in seat:
        if char == 'F':
            row = row[0:math.floor(len(row)/2)]
        elif char == 'B':
            row = row[math.ceil(len(row)/2):]
        elif char == 'R':
            col = col[math.ceil(len(col)/2):]
        elif char == 'L':
            col = col[0:math.floor(len(col)/2)]

    seat_id = row[0] * 8 + col[0]
    print("Boarding Pass: ", seat, "Seat ID: ", seat_id)
    seat_ids.append(seat_id)

seat_ids.sort()
print("Max seat ID: ", max(seat_ids), "Min seat ID: ", min(seat_ids))

# The first value in this list will be a large 
# negative number, this is ok for the problem posed
diff = [a - seat_ids[i-1] for i,a in enumerate(seat_ids)]
pos = diff.index(2, 2, -1)
my_seat = seat_ids[pos] - 1
print("My seat ID is: ", my_seat)
