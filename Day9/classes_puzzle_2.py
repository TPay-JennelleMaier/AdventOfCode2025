

class Coordinate:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __str__(self):
		return "("+str(self.x)+","+str(self.y)+")"

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return self.x == other.x and self.y == other.y

	# area of rectangle formed between these opposite corners
	def calc_area(self, other):
		return (abs(self.x - other.x) + 1) * (abs(self.y - other.y) + 1)



# all lines are vertical or hozitonal
class Line:
	def __init__(self, coord_a, coord_b):
		self.coord_a = coord_a
		self.coord_b = coord_b
		self.is_vertical = self.calc_is_vertical()

	def __str__(self):
		return str(self.coord_a)+"--"+str(self.coord_b)

	def __repr__(self):
		return self.__str__()

	def __eq__(self, other):
		return (self.coord_a == other.coord_a and self.coord_b == other.coord_b) or (self.coord_a == other.coord_b and self.coord_b == other.coord_a)

	def calc_is_vertical(self):
		return self.coord_a.x == self.coord_b.x

	def overlaps_coord(self, coord):
		if self.is_vertical and self.coord_a.x == coord.x:
			return coord.y >= min(self.coord_a.y, self.coord_b.y) and coord.y <= max(self.coord_a.y, self.coord_b.y)
		if not self.is_vertical and self.coord_a.y == coord.y:
			return coord.x >= min(self.coord_a.x, self.coord_b.x) and coord.x <= max(self.coord_a.x, self.coord_b.x)
		return False

	def subsumes_line(self, other):
		if self.is_vertical and other.is_vertical and self.coord_a.x == other.coord_a.x:
			return self.overlaps_coord(other.coord_a) and self.overlaps_coord(other.coord_b)
		if not self.is_vertical and not other.is_vertical and self.coord_a.y == other.coord_a.y:
			return self.overlaps_coord(other.coord_a) and self.overlaps_coord(other.coord_b)
		return False
			
	def overlaps_line(self, other):
		if self.is_vertical and other.is_vertical and self.coord_a.x == other.coord_a.x:
			return self.overlaps_coord(other.coord_a) or self.overlaps_coord(other.coord_b) or other.overlaps_coord(self.coord_a) or other.overlaps_coord(self.coord_b)
		if not self.is_vertical and not other.is_vertical and self.coord_a.y == other.coord_a.y:
			return self.overlaps_coord(other.coord_a) or self.overlaps_coord(other.coord_b) or other.overlaps_coord(self.coord_a) or other.overlaps_coord(self.coord_b)
		if self.is_vertical != other.is_vertical:
			if self.is_vertical:
				point = Coordinate(self.coord_a.x, other.coord_a.y)
				return self.overlaps_coord(point) and other.overlaps_coord(point)
			else:
				point = Coordinate(other.coord_a.x, self.coord_a.y)
				return self.overlaps_coord(point) and other.overlaps_coord(point)
		return False
	


class Shape:
	COLOR_UNKNOWN = 0
	COLOR_REDGREEN = 1
	COLOR_BLACK = 2

	def __init__(self):
		self.lines = []
		self.array_2d = []

	def add_line(self, line):
		self.lines.append(line)

	# returns tuple (min, max)
	def get_x_min_max(self):
		min_x = None
		max_x = None
		for line in self.lines:
			if min_x == None:
				min_x = min(line.coord_a.x, line.coord_b.x)
			else:
				min_x = min(min_x, line.coord_a.x, line.coord_b.x)
			if max_x == None:
				max_x = max(line.coord_a.x, line.coord_b.x)
			else:
				max_x = max(max_x, line.coord_a.x, line.coord_b.x)
		return (min_x, max_x)

	# returns tuple (min, max)
	def get_y_min_max(self):
		min_y = None
		max_y = None
		for line in self.lines:
			if min_y == None:
				min_y = min(line.coord_a.y, line.coord_b.y)
			else:
				min_y = min(min_y, line.coord_a.y, line.coord_b.y)
			if max_y == None:
				max_y = max(line.coord_a.y, line.coord_b.y)
			else:
				max_y = max(max_y, line.coord_a.y, line.coord_b.y)
		return (min_y, max_y)

	# only call this after adding all lines
	def build_array_2d(self):
		self.array_2d = []
		# build blank slate
		(min_x, max_x) = self.get_x_min_max()
		(min_y, max_y) = self.get_y_min_max()
		for r in range(max_y + 3):
			row = []
			for c in range(max_x + 3):
				row.append(Shape.COLOR_UNKNOWN)
			self.array_2d.append(row)
		# search out what is in and out
		# starts where I know we're outside the shape and works inward
		# the middle of the shape ends up not marked, but that is ok
		current_coords = [Coordinate(0,0)]
		while len(current_coords) > 0:
			next_coords = []
			for coord in current_coords:
				if coord.x < 0 or coord.y < 0:
					continue
				if coord.x >= len(self.array_2d[0]) or coord.y >= len(self.array_2d):
					continue
				if self.array_2d[coord.y][coord.x] != Shape.COLOR_UNKNOWN:
					continue
				if self.edge_overlaps_coord(coord):
					self.array_2d[coord.y][coord.x] = Shape.COLOR_REDGREEN
					continue
				self.array_2d[coord.y][coord.x] = Shape.COLOR_BLACK
				next_coords.append(Coordinate(coord.x-1, coord.y))
				next_coords.append(Coordinate(coord.x+1, coord.y))
				next_coords.append(Coordinate(coord.x, coord.y-1))
				next_coords.append(Coordinate(coord.x, coord.y+1))
			current_coords = next_coords;
		# now search inward to turn the remainder to the right color
		# this is needed to catch interior corners
		for r in range(len(self.array_2d)):
			for c in range(len(self.array_2d[r])):
				if self.array_2d[r][c] == Shape.COLOR_UNKNOWN:
					self.array_2d[r][c] = Shape.COLOR_REDGREEN
		
	def print_array_2d(self):
		for row in self.array_2d:
			print("".join([str(x) for x in row]))

	def edge_overlaps_coord(self, coord):
		for line in self.lines:
			if line.overlaps_coord(coord):
				return True
		return False

	def is_valid_rect(self, corner_a, corner_b):
		min_x = min(corner_a.x, corner_b.x)
		max_x = max(corner_a.x, corner_b.x)
		min_y = min(corner_a.y, corner_b.y)
		max_y = max(corner_a.y, corner_b.y)
		# i just need to check the rect edges...but i do need to check all of them
		x = min_x
		while x <= max_x:
			if not self.is_inside_2d_array(Coordinate(x,min_y)):
				return False
			if not self.is_inside_2d_array(Coordinate(x,max_y)):
				return False
			x = x + 1
		y = min_y
		while y <= max_y:
			if not self.is_inside_2d_array(Coordinate(min_x,y)):
				return False
			if not self.is_inside_2d_array(Coordinate(max_x,y)):
				return False
			y = y + 1

		"""
		if not self.is_valid_rect_edge(Line(corner_a, Coordinate(corner_a.x, corner_b.y))):
			return False
		if not self.is_valid_rect_edge(Line(corner_a, Coordinate(corner_a.y, corner_b.x))):
			return False
		if not self.is_valid_rect_edge(Line(corner_b, Coordinate(corner_a.x, corner_b.y))):
			return False
		if not self.is_valid_rect_edge(Line(corner_b, Coordinate(corner_a.y, corner_b.x))):
			return False
		"""
		return True

	def is_valid_rect_edge(self, rect_edge):
		# NOOOOO because the middle of the line could cross outside the shape, gotta check every coord
		if not self.is_inside_ray_cast(rect_edge.coord_a):
			return False
		if not self.is_inside_ray_cast(rect_edge.coord_b):
			return False
		return True

	def is_valid_rect_edge_OLD(self, rect_edge):
		# if any shape edge subsumes the rect edge, then it is valid
		for shape_edge in self.lines:
			if shape_edge.subsumes_line(rect_edge):
				return True
		# only check for partial overlaps after that
		for shape_edge in self.lines:
			if shape_edge.overlaps_line(rect_edge):
				return False
		return True

	def is_inside_2d_array(self, coord):
		return self.array_2d[coord.y][coord.x] == Shape.COLOR_REDGREEN
	
	def is_inside_ray_cast(self, coord):
		# coordinates on the shape edge are ok
		for shape_edge in self.lines:
			if shape_edge.overlaps_coord(coord):
				return True
		# otherwise, do an actual ray cast to an edge
		ray = Line(coord, Coordinate(coord.x, -100))
		count_crossings = 0
		for shape_edge in self.lines:
			if shape_edge.overlaps_line(ray):
				count_crossings = count_crossings + 1
		return count_crossings%2 == 1 #odd number of crossings means coord started inside shape



"""
	def get_outline(self):
		outline = Shape()
		# sample input: guessing on start - make outline lefter and longer than first line
		outline.add_line(self.lines[0].coord_a

		return outline 
"""		



class Outline(Shape):
	def is_valid_rect_edge(self, rect_edge):
		# anything that touches the edges of the outline is invalid
		for shape_edge in self.lines:
			if shape_edge.overlaps_line(rect_edge):
				return False
		return True
	
	@staticmethod
	def build(shape, coords):
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
			#print(c)
			#print(above_overlaps)
			#print(below_overlaps)
			#print(left_overlaps)
			#print(right_overlaps)
			

		outline = Outline()
		outline.add_line(Line(outline_coords[0], outline_coords[-1]))
		i = 0
		while i < len(outline_coords) - 1:
			outline.add_line(Line(outline_coords[i], outline_coords[i+1]))
			i = i + 1
		return outline



"""
class Array2d:
	NO_COLOR = 0

	def __init__(self, row, col):
		self.array_2d = []
		for r in range(row+1):
			array_row = []
			for c in range(col+1):
				array_row.append(Array2d.NO_COLOR)
			self.array_2d.append(array_row)
"""


