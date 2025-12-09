# day 9 puzzle 2
# https://adventofcode.com/2025/day/9#part2

# in the list of input coords, each coord is a red tile
# between each coord and the next coord in the list is a straight line of green tiles
# this wraps from the last coord back to the first
# all tiles inside this closed loop are also green

# now, still find the largest rect with a red tile at each opposite corner
# but the rect must also be entirely made up of red/green tiles

# find the area (in single-tile units) of that rectangle





# so, the edges of the rect cannot cross an edge of this loop/shape
# i'll start there



# next: what if I take an outline one unit outside the valid shape
# then if anything touches that outline, it is invalid
# ahhh not sure how to go about that

# backup and try the dumb solution of making a 2d array of the tilespace
# no this is no good, no matter how i go about it i need to know am i inside the shape or outside it?

# ok got an answer on what is inside/outside the shape
# actual input is taking a long time to run
# still a long time to run

# ok trying 2d array now - i can do it with just edge detection
# nooope, just building the array is taking over an hour on actual input and it still isn't done
# trying to make that part faster



import sys
from classes_puzzle_2 import *





input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

coords = []
for line in full_input.split('\n'):
	(x, y) = line.split(',')
	coords.append(Coordinate(int(x), int(y)))
#print(coords)

shape = Shape()
shape.add_line(Line(coords[0], coords[-1]))
i = 0
while i < len(coords) - 1:
	shape.add_line(Line(coords[i], coords[i+1]))
	i = i + 1
shape.build_array_2d()
#shape.print_array_2d()
print("finished building array_2d")


coord_pairs = [] #tuple(a,b)
i = 0
while i < len(coords) - 1:
	j = i + 1
	while j < len(coords):
		coord_pairs.append( (coords[i], coords[j]) )

		j = j + 1

	i = i + 1
#print(coord_pairs)
print("finished building pairs")


#print("???")
#print(shape.is_valid_rect(Coordinate(9,5), Coordinate(2,3)))
#print("???")



# select only coord-pairs that form valid rect
valid_coord_pairs = [pair for pair in coord_pairs if shape.is_valid_rect(pair[0], pair[1])]
#print(valid_coord_pairs)
print("finished finding valid pairs")

#print("???")
#print(Coordinate(9,5).calc_area(Coordinate(2,3)))
#print("???")


# brute force check all areas at once
valid_coord_pairs.sort(key=lambda pair: pair[0].calc_area(pair[1]))
#print(valid_coord_pairs)

#min_pair = valid_coord_pairs[0]
max_pair = valid_coord_pairs[-1]
#print(min_pair[0].calc_area(min_pair[1]))
#print(max_pair[0].calc_area(max_pair[1]))

answer = max_pair[0].calc_area(max_pair[1])
print("====")
print(answer)



