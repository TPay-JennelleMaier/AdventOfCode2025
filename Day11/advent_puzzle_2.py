# day 11 puzzle 2
# https://adventofcode.com/2025/day/11

# the path with an error passes through "dac" and "fft"

# find all paths from "svr" to "out" which pass through "dac" and "fft"



import sys



class Node:
	def __init__(self, config_line):
		self.name = config_line.split(':')[0]
		self.child_names = config_line.split(':')[1].strip().split(' ')
		self.children = []

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	def build_tree(self, all_nodes):
		if len(self.children) > 0:
			#already got here by another route
			return
		print("build tree: "+self.name)
		for n in all_nodes:
			if n.name in self.child_names:
				self.children.append(n)
				n.build_tree(all_nodes)

	def count_paths(self, target_name, foundDAC, foundFFT):
		print("check "+self.name)

		if self.name == target_name:
			if foundDAC and foundFFT:
				return 1
			return 0
		if self.name == "dac":
			foundDAC = True
		elif self.name  == "fft":
			foundFFT = True

		result = 0
		for n in self.children:
			result = result + n.count_paths(target_name, foundDAC, foundFFT)
		return result




input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()
#print(full_input)


nodes = []
for line in full_input.split('\n'):
	nodes.append(Node(line))
nodes.append(Node("out: "))
print(nodes)

root = [n for n in nodes if n.name == "svr"][0]
#print(root)

root.build_tree(nodes)

answer = root.count_paths("out", False, False)
print("===")
print(answer)

