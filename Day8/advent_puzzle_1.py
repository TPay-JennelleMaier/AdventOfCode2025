# day 8 puzzle 1
# https://adventofcode.com/2025/day/8

# there are junction boxes connected by light-strings
# electricity can travel along the strings and through junction boxes
# which junction boxes need to be connected to provide full connectivity?

# input is a list of (x,y,z) coordinates
# they want to connect junctions that are as close together as possible along a straight line

# for the sample: connect the 10 closest pairs of junctions (even if they are already on the same circuit)
# then find the size of each circuit
# the answer is the size of the 3 biggest circuits multiplied together

# for the actual: connect the 1000 closest pairs and do the same calculation for the answer

# how to narrow down the "closest pair" search quickly?
# for 2d, if the x-axis distance between two points is D1, then the actual distance between the two will be something greater than D1
  # so maybe start with a single-dimension sort?
# but on top of that, it is also a many-to-many problem...
# how many pairs are there in a set of size N?
  # N choose 2 => N(N-1)/2
  # for N=20 this is 190 (sample)
  # for N=1000 this is 499500 (actual)






import sys
import math



TAKE = 1000 #10



class Coordinate:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

	def __str__(self):
		return "("+str(self.x)+", "+str(self.y)+", "+str(self.z)+")"

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y and self.z == other.z

	def __hash__(self):
		return hash(self.__str__())

	def distance(self, other):
		x1 = (self.x - other.x) ** 2
		y1 = (self.y - other.y) ** 2
		z1 = (self.z - other.z) ** 2
		return math.sqrt(x1 + y1 + z1)





input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

coords = []
for line in full_input.split('\n'):
	(x, y, z) = line.split(',')
	coord = Coordinate(int(x), int(y), int(z))
	coords.append(coord)
#print(coords)

coord_pairs = [] #tuple(a,b)
i = 0
while i < len(coords) - 1:
	j = i + 1
	while j < len(coords):
		coord_pairs.append( (coords[i], coords[j]) )

		j = j + 1

	i = i + 1

# brute force check all distance at once
coord_pairs.sort(key=lambda pair: pair[0].distance(pair[1]))
#print(coord_pairs)

# take the top section and determine how large of circuits result
selected_coord_pairs = coord_pairs[:TAKE]
#print(selected_coord_pairs)

# since starting from a pair and merging into that set
# there can be at most two sets merged into it
# so stop searching after two merges
circuits = []
for pair in selected_coord_pairs:
	circuit = set(pair)
	i = 0
	merge_count = 0
	while i < len(circuits) and merge_count < 2:
		if len(circuit.intersection(circuits[i])) > 0:
			circuit.update(circuits[i])
			circuits = circuits[:i] + circuits[i+1:] # remove ith
			merge_count = merge_count + 1
		else:
			i = i + 1
	circuits.append(circuit)
#print(circuits)

circuits.sort(key=lambda c: len(c))

a = len(circuits[-1])
b = len(circuits[-2])
c = len(circuits[-3])
answer = a * b * c
print("======")
print(answer)


