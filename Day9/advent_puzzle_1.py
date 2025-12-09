# day 9 puzzle 1
# https://adventofcode.com/2025/day/9

# given a grid of colored tiles
# find the largest rectangle with a red tile at two opposite corners
# your input is a list of coordinates of the red tiles

# find the area (in single-tile units) of that rectangle

# so, this sounds like pairs again
# check all possible pairs of tiles, to see which makes the largest rectangle





import sys




class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "("+str(self.x)+","+str(self.y)+")"

	def __repr__(self):
		return self.__str__()

	# area of rectangle formed between these opposite corners
	def calc_area(self, other):
		return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)





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

coord_pairs = [] #tuple(a,b)
i = 0
while i < len(coords) - 1:
	j = i + 1
	while j < len(coords):
		coord_pairs.append( (coords[i], coords[j]) )

		j = j + 1

	i = i + 1
#print(coord_pairs)

# brute force check all areas at once
coord_pairs.sort(key=lambda pair: pair[0].calc_area(pair[1]))
#print(coord_pairs)

#min_pair = coord_pairs[0]
max_pair = coord_pairs[-1]
#print(min_pair[0].calc_area(min_pair[1]))
#print(max_pair[0].calc_area(max_pair[1]))

answer = max_pair[0].calc_area(max_pair[1])
print("====")
print(answer)



