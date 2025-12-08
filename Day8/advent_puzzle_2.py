# day 8 puzzle 2
# https://adventofcode.com/2025/day/8#part2

# now connect all junctions until there is one large circuit
# still connect the two closest pairs even if they are already in the same circuit
# keep going until everything is in one circuit

# take the X coordinates of the last two junction boxes connected
# multiply their X coords together to get the answer

# so
# i need to get ALL the junctions into one circuit
# so once an junction is connected to any other junction, I can drop all further possible pairs containing those junctions from the list?
  # no...no because new junctions can still be added in that way
  # I can only drop a pair from the list if BOTH sides are already in the circuit






import sys
import math





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




def update_circuits(circuits, new_pair):
	# since starting from a pair and merging into that set
	# there can be at most two sets merged into it
	# so stop searching after two merges
	circuit = set(new_pair)
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
	return circuits





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


circuits = []
i_pair = 0
while len(circuits) < 1 or (len(circuits[0]) < len(coords) and i_pair < len(coord_pairs)):
	circuits = update_circuits(circuits, coord_pairs[i_pair])
	i_pair = i_pair + 1


last_pair = coord_pairs[i_pair-1]
print(last_pair)

answer = last_pair[0].x * last_pair[1].x
print("======")
print(answer)
