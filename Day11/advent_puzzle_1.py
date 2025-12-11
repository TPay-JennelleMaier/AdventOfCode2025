# day 11 puzzle 1
# https://adventofcode.com/2025/day/11

# get the reactor communicating with the server rack
# input is a list of devices and their outputs
  # device name
  # then list of devices it is sending output to

# start at "you"
# find a path to "out" - no, find EVERY path from "you" to an "out"
# the answer is the number of paths

# ok - hold on - this is a directional graph and i need to count the number of paths from start to the endpoints
# just like in the beam-splitter puzzle earlier
# so i should be able to to the same thing here - start at the end and count backwards


import sys



class Node:
	def __init__(self, config_line):
		self.name = config_line.split(':')[0]
		self.child_names = config_line.split(':')[1].strip().split(' ')

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.__str__()

	def build_tree(self, all_nodes):
		self.children = []
		for n in all_nodes:
			if n.name in self.child_names:
				self.children.append(n)
				n.build_tree(all_nodes)

	def count_paths(self, target_name):
		result = 0
		print("check "+self.name)
		if self.name == target_name:
			return 1
		for n in self.children:
			result = result + n.count_paths(target_name)
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

root = [n for n in nodes if n.name == "you"][0]
#print(root)

root.build_tree(nodes)

answer = root.count_paths("out")
print("===")
print(answer)

