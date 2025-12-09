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

"""
outline_coords = []
prev_above_overlaps = False
prev_below_overlaps = False
prev_left_overlaps = False
prev_right_overlaps = False
for c in coords:
	above_overlaps = shape.edge_overlaps_coord(Coordinate(c.x, c.y+1))
	below_overlaps = shape.edge_overlaps_coord(Coordinate(c.x, c.y-1))
	left_overlaps = shape.edge_overlaps_coord(Coordinate(c.x-1, c.y))
	right_overlaps = shape.edge_overlaps_coord(Coordinate(c.x+1, c.y))
	if above_overlaps and right_overlaps:
		outline_coords.append(Coordinate(c.x-1, c.y-1))
		prev_above_overlaps = above_overlaps
		prev_below_overlaps = below_overlaps
		prev_left_overlaps = left_overlaps
		prev_right_overlaps = right_overlaps
		continue
	if above_overlaps and left_overlaps:
		outline_coords.append(Coordinate(c.x+1, c.y-1))
		prev_above_overlaps = above_overlaps
		prev_below_overlaps = below_overlaps
		prev_left_overlaps = left_overlaps
		prev_right_overlaps = right_overlaps
		continue
	if below_overlaps and right_overlaps:
		outline_coords.append(Coordinate(c.x-1, c.y+1))
		prev_above_overlaps = above_overlaps
		prev_below_overlaps = below_overlaps
		prev_left_overlaps = left_overlaps
		prev_right_overlaps = right_overlaps
		continue
	if below_overlaps and left_overlaps:
		outline_coords.append(Coordinate(c.x+1, c.y+1))
		prev_above_overlaps = above_overlaps
		prev_below_overlaps = below_overlaps
		prev_left_overlaps = left_overlaps
		prev_right_overlaps = right_overlaps
		continue
	if above_overlaps and below_overlaps:
		# use prev settings, from last corner
		if prev_above_overlaps and prev_right_overlaps:
			outline_coords.append(Coordinate(c.x-1, c.y))
			continue
		if prev_above_overlaps and prev_left_overlaps:
			outline_coords.append(Coordinate(c.x+1, c.y))
			continue
		if prev_below_overlaps and prev_right_overlaps:
			outline_coords.append(Coordinate(c.x-1, c.y))
			continue
		if prev_below_overlaps and prev_left_overlaps:
			outline_coords.append(Coordinate(c.x+1, c.y))
			continue
		print("ERROR! A")
	if left_overlaps and right_overlaps:
		# use prev settings, from last corner
		if prev_above_overlaps and prev_right_overlaps:
			outline_coords.append(Coordinate(c.x, c.y-1))
			continue
		if prev_above_overlaps and prev_left_overlaps:
			outline_coords.append(Coordinate(c.x, c.y-1))
			continue
		if prev_below_overlaps and prev_right_overlaps:
			outline_coords.append(Coordinate(c.x, c.y+1))
			continue
		if prev_below_overlaps and prev_left_overlaps:
			outline_coords.append(Coordinate(c.x, c.y+1))
			continue
		print("ERROR! B")
	print("ERROR! C")



outline = Outline()
outline.add_line(Line(outline_coords[0], outline_coords[-1]))
i = 0
while i < len(outline_coords) - 1:
	outline.add_line(Line(outline_coords[i], outline_coords[i+1]))
	i = i + 1

"""


coord_pairs = [] #tuple(a,b)
i = 0
while i < len(coords) - 1:
	j = i + 1
	while j < len(coords):
		coord_pairs.append( (coords[i], coords[j]) )

		j = j + 1

	i = i + 1
#print(coord_pairs)


# select only coord-pairs that form valid rect
valid_coord_pairs = [pair for pair in coord_pairs if shape.is_valid_rect(pair[0], pair[1])]
print(valid_coord_pairs)


# brute force check all areas at once
valid_coord_pairs.sort(key=lambda pair: pair[0].calc_area(pair[1]))
#print(coord_pairs)

#min_pair = coord_pairs[0]
max_pair = coord_pairs[-1]
#print(min_pair[0].calc_area(min_pair[1]))
#print(max_pair[0].calc_area(max_pair[1]))

answer = max_pair[0].calc_area(max_pair[1])
print("====")
print(answer)



