# Day 6 Puzzle 1
# https://adventofcode.com/2025/day/6

# input is a series of columns of math problems
# the math operator is at the bottom of the column: addition (+) or multiplication (*)

# solve each column, then sum the totals together

# the actual input is very wide, but not very long



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

# parse problems
problems = []
is_first_row = True
for line in full_input.split('\n'):
	line = ' '.join(line.split()).strip() # replace any length of whitespace with one space
	#print(line)
	terms = line.split(' ')
	for i in range(len(terms)):
		if is_first_row:
			problems.append(Problem())
		problems[i].add_something(terms[i])
	is_first_row = False


# solve problems
answer = 0
for problem in problems:
	answer = answer + problem.solve()

print("====")
print(answer)
