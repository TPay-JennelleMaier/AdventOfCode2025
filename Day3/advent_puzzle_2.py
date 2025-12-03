# day 3 puzzle 2
# https://adventofcode.com/2025/day/3#part2

# now you can turn on 12 batteries in each bank to make an even bigger joltage


import sys


MAX_LENGTH = 12 #2 #12



def get_joltage(bank):
	index = 0
	digits = []
	for n in range(MAX_LENGTH):
		digits.append(0)
	while index < len(bank):
		for digit_index in range(MAX_LENGTH):
			if index > len(bank) - (MAX_LENGTH - digit_index):
				continue
			if int(bank[index]) > digits[digit_index]:
				digits[digit_index] = int(bank[index])
				clear_index = digit_index + 1
				while clear_index < len(digits):
					digits[clear_index] = 0
					clear_index = clear_index + 1
				break

		index = index + 1
	return "".join([str(d) for d in digits])


input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

answer = 0

for bank in full_input.split('\n'):
	joltage = get_joltage(bank)
	print(joltage)
	print("------")
	answer = answer + int(joltage)

print("======")
print(answer)