# day 7 puzzle 2
# https://adventofcode.com/2025/day/7#part2

# timeline splits - in one timeline the beam split to the left, in another it split to the right
# how many possible journies can the beam take?




import sys





class Path:
	def __init__(self, r, c):
		self.row = r
		self.col = c
		self.is_done = False

		



def all_paths_resolved(paths):
	for path in paths:
		if not path.is_done:
			return False
	return True



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)


array_2d = [list(line) for line in full_input.split('\n')]

#print(array_2d)

paths = []

# init first path
c = 0
while c < len(array_2d[0]):
	if array_2d[0][c] == 'S':
		paths.append(Path(1, c))
		break
	c = c + 1

# iterate until all paths are resolved
while not all_paths_resolved(paths):
	for path in paths:
		if path.is_done:
			continue
		# step
		if path.row + 1 >= len(array_2d):
			path.is_done = True
			continue
		if array_2d[path.row+1][path.col] == '.':
			path.row = path.row + 1
			continue
		if array_2d[path.row+1][path.col] == '^':
			new_path = Path(path.row+1, path.col-1)
			path.row = path.row + 1
			path.col = path.col + 1
			paths.append(new_path)


# seeing that brute force on the actual input takes a while to run...



answer = len(paths)
print("====")
print(answer)

