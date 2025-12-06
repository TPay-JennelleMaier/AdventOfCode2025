# Day 6 Puzzle 2
# https://adventofcode.com/2025/day/6#part2

# a number written as 
# 3
# 2
# 4
# equals 324, read top to bottom

# and the spaces matter, because the way the digits line up in columns matters

# so, I think I want to rotate the whole input 90 degrees counterclockwise
# then a full blank line will indicate a break between problems
# and each number will read left-to-right as I'm used to


import sys



class Problem:
	def __init__(self):
		self.numbers = []
		self.operator = ""

	def add_something(self, thing):
		if thing == '+' or thing ==  '*':
			self.set_operator(thing)
		else:
			self.add_number(int(thing))

	def add_number(self, n):
		self.numbers.append(n)

	def set_operator(self, op):
		self.operator = op

	def solve(self):
		if self.operator == "":
			return 0 #empty problem - ignore it

		if self.operator == '+':
			answer = 0
			for n in self.numbers:
				answer = answer + n
			return answer
		else:
			answer = 1
			for n in self.numbers:
				answer = answer * n
			return answer





input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)


# rotate full input 90 degrees counterclockwise
# 1. convert to 2d array of characters
array_2d = []
for line in full_input.split('\n'):
	array_2d.append(list(line))
#print(array_2d)
# 2. rotate the 2d array
array_2d_rotated = []
col = len(array_2d[0]) - 1
while col >= 0:
	row = []
	for r in range(len(array_2d)):
		row.append(array_2d[r][col])
	array_2d_rotated.append(row)
	col = col - 1
#print(array_2d_rotated)


# parse problems
problems = [Problem()]
for row in array_2d_rotated:
	line = ''.join(row).strip()
	if line == "": # empty line is a break between problems
		problems.append(Problem())
		continue
	#print(line)
	problem = problems[-1]
	if '+' in line:
		problem.set_operator('+')
		line = line.replace('+', '')
	if '*' in line:
		problem.set_operator('*')
		line = line.replace('*', '')
	problem.add_number(int(line))	
	

# solve problems
answer = 0
for problem in problems:
	answer = answer + problem.solve()

print("====")
print(answer)
