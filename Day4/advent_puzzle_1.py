# day 4 puazzle 1
# https://adventofcode.com/2025/day/4

# optimize the work of the forklifts
# @ means roll of paper
# your input is a 2d grid of "@" and "."
# a forklift can only reach a roll if there are fewer than 4 rolls in the 8-adjacent squares around it

# count up how many rolls of paper can currently be accessed by a forklift


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

answer = 0

for y in range(len(grid)):
	for x in range(len(grid[y])):
		#print(grid[y][x])
		if grid[y][x] != ROLL_CHAR:
			continue
		if is_accessible(x, y, grid):
			#print(str(x)+","+str(y)+" is accessible")
			answer = answer + 1

print("======")
print(answer)