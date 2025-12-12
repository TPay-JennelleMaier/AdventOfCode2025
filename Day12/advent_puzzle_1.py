# day 12 puzzle 1
# https://adventofcode.com/2025/day/12

# need to fit the presents under the tree
# fit them into a 2d grid

# puzzle input has a list of the types-of-shapes of present ("#" is part of the present and "." is not)
# then it has the size of regions with their size and how many of each shape-type needs to be fit into it
  # presents can be rotated and flipped

# how many of the regions CAN fit the presents listed?




# i'm going to just do brute force on this



import sys


class Array2d:
	def __init__(self, array_2d):
		self.array_2d = array_2d # list of lists, array_2d[row][col]

	def __str__(self):
		return Array2d.str_grid(self.array_2d) + "\n"
	
	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return str(self) == str(other)

	@staticmethod
	def str_grid(array_2d):
		return "\n".join([ Array2d.str_row(row) for row in array_2d])

	@staticmethod
	def str_row(row_2d):
		return "".join([str(int(x)) for x in row_2d])

	# returns a new instance
	def rotate_once(self):
		result = []
		c = len(self.array_2d)-1
		while c >= 0:
			new_row = []
			for r in range(len(self.array_2d)):
				new_row.append(self.array_2d[r][c])
			c = c - 1
			result.append(new_row)				
		return Array2d(result)

	# returns a new instance
	def flip_once(self):
		result = []
		for row in self.array_2d:
			new_row = []
			c = len(row)-1
			while c >= 0:
				new_row.append(row[c])
				c = c - 1
			result.append(new_row)				
		return Array2d(result)
		
		




class PresentType:
	def __init__(self, index, array_2d_shape):
		self.index = index
		self.array_2d = Array2d(array_2d_shape) # 2d array of True/False for where the present is located
		self.variations = []
		self.determine_variations()

	def __str__(self):
		return str(self.index)+":\n"+str(self.array_2d) + "\n"
	
	def __repr__(self):
		return self.__str__()

	def determine_variations(self):
		self.variations.append(self.array_2d)
		# once
		turned = self.array_2d.rotate_once()
		if not turned in self.variations:
			self.variations.append(turned)
		# twice
		turned = turned.rotate_once()
		if not turned in self.variations:
			self.variations.append(turned)
		# three times
		turned = turned.rotate_once()
		if not turned in self.variations:
			self.variations.append(turned)
		# then flip the original and rotate it all again
		flipped = self.array_2d.flip_once()
		if not flipped in self.variations:
			self.variations.append(flipped)
		# once
		turned = flipped.rotate_once()
		if not turned in self.variations:
			self.variations.append(turned)
		# twice
		turned = turned.rotate_once()
		if not turned in self.variations:
			self.variations.append(turned)
		# three times
		turned = turned.rotate_once()
		if not turned in self.variations:
			self.variations.append(turned)
		
		print(self.variations)
		print("----")
		
		



class Region:
	def __init__(self, width, height):
		self.array_2d = [ [False]*width ] * height
		self.present_types = []
		self.is_possible = False

	def __str__(self):
		return str(len(self.array_2d))+"x"+str(len(self.array_2d[0])) + " with " + str(len(self.present_types)) + " presents\n"
	
	def __repr__(self):
		return self.__str__()

	def add_present_type(self, present_type, quantity):
		self.present_types.extend([present_type]*quantity)

	def determine_if_possible(self):
		pass





input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)


present_types = []
regions = []
stored_index = None
stored_shape_lines = []
for line in full_input.split('\n'):
	if "x" in line:
		(width, height) = line.split(':')[0].split('x')
		region = Region(int(width), int(height))
		quantities = line.split(':')[1].strip().split(' ')
		for i in range(len(quantities)):
			region.add_present_type(present_types[i], int(quantities[i]))
		regions.append(region)		
		continue
	if line == "":
		#end of a shape
		present_types.append(PresentType(stored_index, stored_shape_lines))
		stored_shape_lines = []
		continue
	if ":" in line:
		stored_index = int(line.split(':')[0])
		continue
	stored_shape_lines.append( [x=='#' for x in line] )

print(present_types)
print(regions)


for region in regions:
	region.determine_if_possible()

answer = len([r for r in regions if r.is_possible])
print("=====")
print(answer)
