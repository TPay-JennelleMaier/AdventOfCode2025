import unittest
from classes_puzzle_2 import *

class Test_Line(unittest.TestCase):
	def test_init(self):
		line = Line(Coordinate(1, 3), Coordinate(1, 7))
		self.assertEqual(line.is_vertical, True)

		line = Line(Coordinate(1, 3), Coordinate(5, 3))
		self.assertEqual(line.is_vertical, False)

	def test_overlaps_coord(self):
		line = Line(Coordinate(1, 3), Coordinate(1, 7)) # vertical
		self.assertEqual(line.overlaps_coord(Coordinate(1, 3)), True) # on end
		self.assertEqual(line.overlaps_coord(Coordinate(1, 7)), True) # on end
		self.assertEqual(line.overlaps_coord(Coordinate(1, 5)), True) # in middle
		self.assertEqual(line.overlaps_coord(Coordinate(1, 2)), False) # too low
		self.assertEqual(line.overlaps_coord(Coordinate(1, 8)), False) # too high
		self.assertEqual(line.overlaps_coord(Coordinate(2, 6)), False) # not at all

		line = Line(Coordinate(1, 3), Coordinate(5, 3)) # horizontal
		self.assertEqual(line.overlaps_coord(Coordinate(1, 3)), True) # on end
		self.assertEqual(line.overlaps_coord(Coordinate(5, 3)), True) # on end
		self.assertEqual(line.overlaps_coord(Coordinate(4, 3)), True) # in middle
		self.assertEqual(line.overlaps_coord(Coordinate(0, 3)), False) # too low
		self.assertEqual(line.overlaps_coord(Coordinate(7, 3)), False) # too high
		self.assertEqual(line.overlaps_coord(Coordinate(2, 6)), False) # not at all

	def test_subsumes_line(self):
		line_a = Line(Coordinate(1, 3), Coordinate(1, 7)) # vertical
		line_b = Line(Coordinate(1, 3), Coordinate(1, 7)) # vertical - exact
		line_e = Line(Coordinate(1, 4), Coordinate(1, 5)) # vertical subsumed
		line_f = Line(Coordinate(1, 0), Coordinate(1, 9)) # vertical subsumes
		self.assertEqual(line_a.subsumes_line(line_b), True)
		self.assertEqual(line_a.subsumes_line(line_e), True)
		self.assertEqual(line_a.subsumes_line(line_f), False)

		line_a = Line(Coordinate(1, 3), Coordinate(5, 3)) # horizontal
		line_b = Line(Coordinate(1, 3), Coordinate(5, 3)) # horizontal - exact
		line_e = Line(Coordinate(2, 3), Coordinate(4, 3)) # horizontal subsumed
		line_f = Line(Coordinate(0, 3), Coordinate(6, 3)) # horizontal subsumes
		self.assertEqual(line_a.subsumes_line(line_b), True)
		self.assertEqual(line_a.subsumes_line(line_e), True)
		self.assertEqual(line_a.subsumes_line(line_f), False)


	def test_overlaps_line(self):
		line_a = Line(Coordinate(1, 3), Coordinate(1, 7)) # vertical
		line_b = Line(Coordinate(1, 3), Coordinate(1, 7)) # vertical - exact
		line_c = Line(Coordinate(1, 4), Coordinate(1, 9)) # vertical partial above
		line_d = Line(Coordinate(1, 2), Coordinate(1, 4)) # vertical partial below
		line_e = Line(Coordinate(1, 4), Coordinate(1, 5)) # vertical subsumed
		line_f = Line(Coordinate(1, 0), Coordinate(1, 9)) # vertical subsumes
		line_g = Line(Coordinate(1, 9), Coordinate(1, 11)) # vertical in line but no overlap
		line_h = Line(Coordinate(2, 3), Coordinate(2, 7)) # vertical parallel
		self.assertEqual(line_a.overlaps_line(line_b), True)
		self.assertEqual(line_a.overlaps_line(line_c), True)
		self.assertEqual(line_a.overlaps_line(line_d), True)
		self.assertEqual(line_a.overlaps_line(line_e), True)
		self.assertEqual(line_a.overlaps_line(line_f), True)
		self.assertEqual(line_a.overlaps_line(line_g), False)
		self.assertEqual(line_a.overlaps_line(line_h), False)

		line_a = Line(Coordinate(1, 3), Coordinate(5, 3)) # horizontal
		line_b = Line(Coordinate(1, 3), Coordinate(5, 3)) # horizontal - exact
		line_c = Line(Coordinate(0, 3), Coordinate(2, 3)) # horizontal partial left
		line_d = Line(Coordinate(3, 3), Coordinate(8, 3)) # horizontal partial right
		line_e = Line(Coordinate(2, 3), Coordinate(4, 3)) # horizontal subsumed
		line_f = Line(Coordinate(0, 3), Coordinate(6, 3)) # horizontal subsumes
		line_g = Line(Coordinate(6, 3), Coordinate(9, 3)) # horizontal in line but no overlap
		line_h = Line(Coordinate(1, 4), Coordinate(5, 4)) # horizontal parallel
		self.assertEqual(line_a.overlaps_line(line_b), True)
		self.assertEqual(line_a.overlaps_line(line_c), True)
		self.assertEqual(line_a.overlaps_line(line_d), True)
		self.assertEqual(line_a.overlaps_line(line_e), True)
		self.assertEqual(line_a.overlaps_line(line_f), True)
		self.assertEqual(line_a.overlaps_line(line_g), False)
		self.assertEqual(line_a.overlaps_line(line_h), False)

		line_a = Line(Coordinate(1, 3), Coordinate(1, 7)) # vertical
		line_b = Line(Coordinate(1, 3), Coordinate(5, 3)) # horizontal - corner to corner
		line_c = Line(Coordinate(1, 5), Coordinate(4, 5)) # horizontal - corner to middle
		line_d = Line(Coordinate(0, 4), Coordinate(5, 4)) # horizontal - middle to middle
		line_e = Line(Coordinate(2, 3), Coordinate(5, 3)) # horizontal - corner to not corner
		line_f = Line(Coordinate(2, 5), Coordinate(4, 5)) # horizontal - corner to not middle
		line_g = Line(Coordinate(2, 4), Coordinate(5, 4)) # horizontal - middle to not middle
		self.assertEqual(line_a.overlaps_line(line_b), True)
		self.assertEqual(line_a.overlaps_line(line_c), True)
		self.assertEqual(line_a.overlaps_line(line_d), True)
		self.assertEqual(line_a.overlaps_line(line_e), False)
		self.assertEqual(line_a.overlaps_line(line_f), False)
		self.assertEqual(line_a.overlaps_line(line_g), False)

		#  TODO same horizontal tests if needed

class Test_Shape(unittest.TestCase):
	def test_edge_overlaps_coord(self):
		shape = Shape()
		shape.add_line(Line(Coordinate(0,0), Coordinate(0,3)))
		shape.add_line(Line(Coordinate(0,3), Coordinate(3,3)))
		shape.add_line(Line(Coordinate(3,3), Coordinate(3,6)))
		shape.add_line(Line(Coordinate(3,6), Coordinate(6,6)))
		shape.add_line(Line(Coordinate(6,6), Coordinate(6,0)))
		shape.add_line(Line(Coordinate(6,0), Coordinate(0,0)))

		self.assertEqual(shape.edge_overlaps_coord(Coordinate(0,0)), True) # matches corner
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(1,0)), True)
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(0,1)), True)
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(-1,0)), False)
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(0,-1)), False)

		self.assertEqual(shape.edge_overlaps_coord(Coordinate(3,3)), True) # matches corner
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(2,3)), True)
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(3,4)), True)
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(4,3)), False)
		self.assertEqual(shape.edge_overlaps_coord(Coordinate(3,2)), False)

	def test_is_valid_rect_edge(self):
		shape = Shape()
		shape.add_line(Line(Coordinate(0,0), Coordinate(0,3)))
		shape.add_line(Line(Coordinate(0,3), Coordinate(3,3)))
		shape.add_line(Line(Coordinate(3,3), Coordinate(3,6)))
		shape.add_line(Line(Coordinate(3,6), Coordinate(6,6)))
		shape.add_line(Line(Coordinate(6,6), Coordinate(6,0)))
		shape.add_line(Line(Coordinate(6,0), Coordinate(0,0)))

		self.assertEqual(shape.is_valid_rect_edge(Line(Coordinate(0,3), Coordinate(3,3))), True) # exact match
		self.assertEqual(shape.is_valid_rect_edge(Line(Coordinate(1,3), Coordinate(2,3))), True) # subsumed by shape

	def test_is_valid_rect(self):
		shape = Shape()
		shape.add_line(Line(Coordinate(0,0), Coordinate(0,3)))
		shape.add_line(Line(Coordinate(0,3), Coordinate(3,3)))
		shape.add_line(Line(Coordinate(3,3), Coordinate(3,6)))
		shape.add_line(Line(Coordinate(3,6), Coordinate(6,6)))
		shape.add_line(Line(Coordinate(6,6), Coordinate(6,0)))
		shape.add_line(Line(Coordinate(6,0), Coordinate(0,0)))

		self.assertEqual(shape.is_valid_rect(Coordinate(0,0), Coordinate(3,3)), True)
		###self.assertEqual(shape.is_valid_rect(Coordinate(3,6), Coordinate(6,6)), True) # single line rect - skipping for now
		###self.assertEqual(shape.is_valid_rect(Coordinate(3,6), Coordinate(0,6)), True) # oh shit - rect edge extends INTO valid space
		self.assertEqual(shape.is_valid_rect(Coordinate(3,3), Coordinate(6,6)), True)


class Test_Outline(unittest.TestCase):
	def test_build_from_coords(self):
		coords = [Coordinate(0,0), Coordinate(0,3), Coordinate(3,3), Coordinate(3,6), Coordinate(6,6), Coordinate(6,0)]
		shape = Shape()
		shape.add_line(Line(Coordinate(0,0), Coordinate(0,3)))
		shape.add_line(Line(Coordinate(0,3), Coordinate(3,3)))
		shape.add_line(Line(Coordinate(3,3), Coordinate(3,6)))
		shape.add_line(Line(Coordinate(3,6), Coordinate(6,6)))
		shape.add_line(Line(Coordinate(6,6), Coordinate(6,0)))
		shape.add_line(Line(Coordinate(6,0), Coordinate(0,0)))

		outline = Outline.build(shape, coords)
		print(outline.lines)

		#self.assertEqual(shape.is_valid_rect_edge(Line(Coordinate(0,3), Coordinate(3,3))), True) # exact match

		


if __name__ == "__main__":
    unittest.main()