# day 4 puazzle 2
# https://adventofcode.com/2025/day/4#part2

# now, once a roll is accessible it can also be removed, which makes more accessible
# how many total rolls can be removed if this is repeated over and over again?


import sys


ROLL_CHAR = "@"


def is_in_range(x, y, grid):
	if x < 0 or y < 0:
		return False
	if y >= len(grid):
		return False
	if x >= len(grid[0]):
		return False
	return True



def count_adjacent_rolls(x, y, grid):
	result = 0
	if is_in_range(x-1, y-1, grid) and grid[y-1][x-1] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x, y-1, grid) and grid[y-1][x] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x+1, y-1, grid) and grid[y-1][x+1] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x-1, y, grid) and grid[y][x-1] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x+1, y, grid) and grid[y][x+1] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x-1, y+1, grid) and grid[y+1][x-1] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x, y+1, grid) and grid[y+1][x] == ROLL_CHAR:
		result = result + 1
	if is_in_range(x+1, y+1, grid) and grid[y+1][x+1] == ROLL_CHAR:
		result = result + 1
	#print(str(x)+","+str(y)+" has "+str(result)+" adjacent rolls")
	return result





def is_accessible(x, y, grid):
	return count_adjacent_rolls(x, y, grid) < 4
	



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

grid = full_input.split('\n') # one string per row
grid = [list(row) for row in grid] # list of lists of chars

answer = 0

change_made = True
while change_made:
	change_made = False
	for y in range(len(grid)):
		for x in range(len(grid[y])):
			#print(grid[y][x])
			if grid[y][x] != ROLL_CHAR:
				continue
			if is_accessible(x, y, grid):
				#print(str(x)+","+str(y)+" is accessible")
				answer = answer + 1
				grid[y][x] = '.'
				change_made = True

print("======")
print(answer)