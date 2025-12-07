# day 7 puzzle 2
# https://adventofcode.com/2025/day/7#part2

# timeline splits - in one timeline the beam split to the left, in another it split to the right
# how many possible journies can the beam take?

# ok brute force solution is too slow in actual input
# what if we convert the input into a binary tree based on which nodes will split again?




# ....this one is also taking a while on actual input


import sys



class Node:
	def __init__(self, row, col):
		self.row = row
		self.col = col
		self.left_child = None
		self.right_child = None
		
	def build_tree(self, array_2d):
		# find the next splitter, or end of diagram
		while self.row <= len(array_2d)-1 and array_2d[self.row][self.col] == '.':
			self.row = self.row + 1
		if self.row >= len(array_2d):
			return #end of file
		if array_2d[self.row][self.col] == '^':
			self.left_child = Node(self.row+1, self.col-1)
			self.right_child = Node(self.row+1, self.col+1)
			self.left_child.build_tree(array_2d)
			self.right_child.build_tree(array_2d)
		

	def count_paths(self):
		if self.left_child == None and self.right_child == None:
			return 1
		return self.left_child.count_paths() + self.right_child.count_paths()




input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)


array_2d = [list(line) for line in full_input.split('\n')]

# init first node
root = None
c = 0
while c < len(array_2d[0]):
	if array_2d[0][c] == 'S':
		root = Node(1, c)
		break
	c = c + 1


# build binary tree
root.build_tree(array_2d)


answer = root.count_paths()
print("====")
print(answer)

