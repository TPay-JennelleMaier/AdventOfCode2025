# day 7 puzzle 1
# https://adventofcode.com/2025/day/7

# error code 0H-N0
# see diagram input of the techyon manifold
# start at "S"
# move downward through "."s
# at a splitter "^" the beam splits in two and continues downward on the left and right
# if two beams are going down the same column, it is really just one beam

# ...how did they get "21 splits" out of their example?
# there are 22 "^" that were hit
# clarify: when the beam hits ^ it stops and two new beams start on each side of it
# oh ok! there are 22 ^ but one was not hit at all! so the answer was 21
# so I need to count how many ^ get hit




import sys


input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)


array_2d = [list(line) for line in full_input.split('\n')]

#print(array_2d)

# setting "^" to "x" when it is hit
# working top to bottom
r = 0
while r < len(array_2d) - 1: #skip last row
	c = 0
	while c < len(array_2d[r]):
		if array_2d[r][c] == 'S':
			array_2d[r+1][c] = '|'
		elif array_2d[r][c] == '|':
			if array_2d[r+1][c] == '.':
				array_2d[r+1][c] = '|'
			elif array_2d[r+1][c] == '^':
				array_2d[r+1][c] = 'x'
				array_2d[r+1][c-1] = '|'
				array_2d[r+1][c+1] = '|'
		c = c + 1
	r = r + 1


# count "x" (used splitters)
answer = 0
for row in array_2d:
	for cell in row:
		if cell == 'x':
			answer = answer + 1

print("====")
print(answer)

