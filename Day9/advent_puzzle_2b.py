# day 9 puzzle 2
# https://adventofcode.com/2025/day/9#part2

# in the list of input coords, each coord is a red tile
# between each coord and the next coord in the list is a straight line of green tiles
# this wraps from the last coord back to the first
# all tiles inside this closed loop are also green

# now, still find the largest rect with a red tile at each opposite corner
# but the rect must also be entirely made up of red/green tiles

# find the area (in single-tile units) of that rectangle



# i need a new approach
# the list of corners coordinates is short - that part is not the problem
# the issues is that the numbers are large
# there are 496 lines in my input
  # N choose 2 of 496 => 122760 possible pairs

# storing the "already confirmed" good inside coordinates take even longer than checking anew

# it is taking a while to solve even some of the pairs - visibly slow by 140th pair
  # memory usage is not increasing visibly in Activity Monitor
# returning to method "is_valid_rect_edge"
  # because it is /fast/...not accurate yet but let's see if I can fix that without slowing it down

# found another old typo causing an error

# got an answer but it was too low: 1292238828 from pair ((94619,48466), (4512,34126))

# should I try to make an outline again? if anything touched that, it'd be invalid for sure
# ...


import sys
from classes_puzzle_2b import *





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



# select only coord-pairs that form valid rect
valid_coord_pairs = [pair for pair in coord_pairs if shape.is_valid_rect(pair[0], pair[1])]
#print(valid_coord_pairs)
print("finished finding valid pairs")


# brute force check all areas at once
valid_coord_pairs.sort(key=lambda pair: pair[0].calc_area(pair[1]))
#print(valid_coord_pairs)

#min_pair = valid_coord_pairs[0]
max_pair = valid_coord_pairs[-1]
print("max pair")
print(max_pair)

answer = max_pair[0].calc_area(max_pair[1])
print("====")
print(answer)



