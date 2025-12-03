# day 3 puzzle 1
# https://adventofcode.com/2025/day/3

# joltage rating of batteries, values 1-9
# each row is one bank of batteries
# turn on just two batteries in each bank
# if bank = 12345 and you turn on 2 and 4 then the resulting joltage is 2 concat 4  = 24
# find the largest possible joltage each bank can produce

# so I want the largest first digit that is not in last place in the bank
# then largest second digit that is to the right of that

# the answer is the sum of each bank's joltage


import sys



def get_joltage(bank):
	index = 0
	first_digit = 0
	second_digit = 0
	while index < len(bank):
		if index < len(bank) - 1 and int(bank[index]) > first_digit:
			first_digit = int(bank[index])
			second_digit = 0
		elif int(bank[index]) > second_digit:
			second_digit = int(bank[index])
		index = index + 1
	return str(first_digit) + str(second_digit)


input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

answer = 0

for bank in full_input.split('\n'):
	joltage = get_joltage(bank)
	print(joltage)
	answer = answer + int(joltage)

print(answer)