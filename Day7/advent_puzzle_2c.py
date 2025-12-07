# day 7 puzzle 2
# https://adventofcode.com/2025/day/7#part2

# timeline splits - in one timeline the beam split to the left, in another it split to the right
# how many possible journies can the beam take?

# ok brute force solution is too slow in actual input
# what if we convert the input into a binary tree based on which nodes will split again?

# ok second attempt with tree structure also did not work fast enough
# i have a new idea based on the path counter from B, though
# if i start at the bottom of the diagram, and sum the paths upward, it is N time and I worked out on paper that this works on the sample input



# result came very fast for actual input this time!!!


import sys



def search_downward(r, c, array_2d):
	if r >= len(array_2d):
		return 1 #always a default of 1 path
	if array_2d[r][c] == '.':
		return search_downward(r+1, c, array_2d)
	return array_2d[r][c]


def get_path_count(r, c, array_2d):
	#assumes the current space is a "^"
	return search_downward(r+1, c-1, array_2d) + search_downward(r+1, c+1, array_2d)	



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)


array_2d = [list(line) for line in full_input.split('\n')]


# i will start from the bottom row and go up
# and i will replace each "^" with the integrate count of its possible paths
# which will sum together as they work their way up


last_path_count = 0
r = len(array_2d) - 1
while r >= 0:
	
	c = 0
	while c < len(array_2d[r]):
		if array_2d[r][c] == '^':
			array_2d[r][c] = get_path_count(r, c, array_2d)
			last_path_count = array_2d[r][c]

		c  = c + 1

	r = r - 1




print("====")
print(last_path_count)

