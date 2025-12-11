# day 11 puzzle 2
# https://adventofcode.com/2025/day/11

# the path with an error passes through "dac" and "fft"

# find all paths from "svr" to "out" which pass through "dac" and "fft"

# should I make a copy of the whole tree below "dac", and then do the same for everything below "fft"? so those counts are separate?
# start at the ends and work back up the tree?
# mark the paths first? can i cull out the routes that don't lead to both "dac" and "fft"?
  # brainstorming
  # start at "dac" - i can jump directly to it from the node list
  # send a marker up the tree till it reaches root
  # do the same for "fft"



import sys



class Node:
	def __init__(self, config_line):
		self.name = config_line.split(':')[0]
		self.child_names = config_line.split(':')[1].strip().split(' ')
		self.children = []
		self.markers = []
		self.path_count = None

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


	def mark_path_up(self, all_nodes, target_name):
		if target_name in self.markers:
			return
		print("place marker: "+self.name+": "+target_name)
		self.markers.append(target_name)
		for parent in [n for n in all_nodes if self.name in n.child_names]:
			parent.mark_path_up(all_nodes, target_name)


	def count_paths(self, target_name, needed_markers):
		#print("check "+self.name)

		for needed_marker in needed_markers:
			if not needed_marker in self.markers:
				return 0

		if self.name == target_name:
			return 1

		next_markers = needed_markers.copy()
		if self.name in next_markers:
			next_markers.remove(self.name)

		result = 0
		for n in self.children:
			result = result + n.count_paths(target_name, next_markers)
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
print("finished building tree")

dac = [n for n in nodes if n.name == "dac"][0]
fft = [n for n in nodes if n.name == "fft"][0]
dac.mark_path_up(nodes, "dac")
fft.mark_path_up(nodes, "fft")
print("finished placing markers")

#print(root.markers)

answer = root.count_paths("out", ["dac", "fft"])
print("===")
print(answer)
