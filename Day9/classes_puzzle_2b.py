

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

	"""
	# if lines don't overlap, returns empty list
	# if lines do overlap, returns the one or two points on "other" that are just-off-of "self"
	def coming_off_overlap(self, other):
	"""	

	# returns a list of coords, not boolean
	# if empty, then self does not partially-subsume other
	# if filled (1 or 2 coords) then those are the coord just past the ends of the self
	def partially_subsumes_line(self, other):
		results = []
		if self.is_vertical and other.is_vertical and self.coord_a.x == other.coord_a.x:
			if other.overlaps_coord(self.coord_a):
				above_coord = Coordinate(self.coord_a.x, self.coord_a.y+1)
				if other.overlaps_coord(above_coord) and not self.overlaps_coord(above_coord):
					results.append(above_coord)
				below_coord = Coordinate(self.coord_a.x, self.coord_a.y-1)
				if other.overlaps_coord(below_coord) and not self.overlaps_coord(below_coord):
					results.append(below_coord)
			if other.overlaps_coord(self.coord_b):
				above_coord = Coordinate(self.coord_b.x, self.coord_b.y+1)
				if other.overlaps_coord(above_coord) and not self.overlaps_coord(above_coord):
					results.append(above_coord)
				below_coord = Coordinate(self.coord_b.x, self.coord_b.y-1)
				if other.overlaps_coord(below_coord) and not self.overlaps_coord(below_coord):
					results.append(below_coord)
		if not self.is_vertical and not other.is_vertical and self.coord_a.y == other.coord_a.y:
			if other.overlaps_coord(self.coord_a):
				left_coord = Coordinate(self.coord_a.x-1, self.coord_a.y)
				if other.overlaps_coord(left_coord) and not self.overlaps_coord(left_coord):
					results.append(left_coord)
				right_coord = Coordinate(self.coord_a.x+1, self.coord_a.y)
				if other.overlaps_coord(right_coord) and not self.overlaps_coord(right_coord):
					results.append(right_coord)
			if other.overlaps_coord(self.coord_b):
				left_coord = Coordinate(self.coord_b.x-1, self.coord_b.y)
				if other.overlaps_coord(left_coord) and not self.overlaps_coord(left_coord):
					results.append(left_coord)
				right_coord = Coordinate(self.coord_b.x+1, self.coord_b.y)
				if other.overlaps_coord(right_coord) and not self.overlaps_coord(right_coord):
					results.append(right_coord)
		return results

	# returns True is lines cross, but the overlap is just on one end of "other"
	# additional: it is also ok for just one end of "shape" to be overlapped - if there is an error then another edge will catch it...i think
	def overlaps_line_just_on_end(self, other):
		if self.is_vertical != other.is_vertical:
			if self.is_vertical:
				point = Coordinate(self.coord_a.x, other.coord_a.y)
				return self.overlaps_coord(point) and other.overlaps_coord(point) and (other.coord_a == point or other.coord_b == point or self.coord_a == point or self.coord_b == point)
			else:
				point = Coordinate(other.coord_a.x, self.coord_a.y)
				return self.overlaps_coord(point) and other.overlaps_coord(point) and (other.coord_a == point or other.coord_b == point or self.coord_a == point or self.coord_b == point)
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

	def __init__(self):
		self.lines = []
		self.count_is_valid_rect = 0
		self.confirmed_valid_coords = []

	def add_line(self, line):
		self.lines.append(line)

	def build_outline(self):
		# dunno which side of the line to start on
		# so solve for both, and keep the one that is longer
		pass

	def edge_overlaps_coord(self, coord):
		for line in self.lines:
			if line.overlaps_coord(coord):
				return True
		return False

	def is_valid_rect(self, corner_a, corner_b):
		self.count_is_valid_rect = self.count_is_valid_rect + 1
		print(self.count_is_valid_rect)
		print("from "+str(corner_a)+" to "+str(corner_b))
		if not self.is_valid_rect_edge(Line(corner_a, Coordinate(corner_a.x, corner_b.y))):
			return False
		if not self.is_valid_rect_edge(Line(corner_a, Coordinate(corner_b.x, corner_a.y))):
			return False
		if not self.is_valid_rect_edge(Line(corner_b, Coordinate(corner_a.x, corner_b.y))):
			return False
		if not self.is_valid_rect_edge(Line(corner_b, Coordinate(corner_b.x, corner_a.y))):
			return False
		
		return True

	def is_valid_rect_edge(self, rect_edge):
		# if any shape edge subsumes the rect edge, then it is valid
		for shape_edge in self.lines:
			if shape_edge.subsumes_line(rect_edge):
				return True
		for shape_edge in self.lines:
			# what is the shape_edge /partially/ subsumes the rect but the extra rect bit is on the /inside/ of the shape?
			# i could determine just the point(s) on the rect that are just off of the shape, and ray_cast check them
			partial_result = shape_edge.partially_subsumes_line(rect_edge)
			for coord in partial_result:
				if not self.is_inside_ray_cast(coord):
					return False
			if len(partial_result) > 0:
				continue
			# only check for partial overlaps after that
			if shape_edge.overlaps_line_just_on_end(rect_edge):
				continue
			if shape_edge.overlaps_line(rect_edge):
				print("fail 3")
				print(shape_edge)
				print(rect_edge)
				return False
		return True
	
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
		is_valid = count_crossings%2 == 1 #odd number of crossings means coord started inside shape
		return is_valid



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


