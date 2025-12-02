# day 2 puzzle 1
# https://adventofcode.com/2025/day/2
# identifying invalid product ideas
# inputs is a comma-seperated list of ranges, all on one line
# a range is NUM-NUM
# the invalid ids are sequences of repeated digits (twice repeated only) like 55 and 6464 and 123123
# find all invalid ids, no matter where in a range they appear - including in the middle of range!
# sum them to get the answer



import sys
import re


# returns TRUE if text is the same thing repeated twice
def is_doubled(text):
	length = len(text)
	if length%2 == 1:
		return False
	half = int(length / 2)
	return text[:half] == text[half:]



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

##input_ids = re.split(',|-', full_input) #split on "," or "-"
input_ranges = full_input.split(',')

answer = 0

for ra in input_ranges:
	min = int(ra.split('-')[0])
	max = int(ra.split('-')[1])
	while min <= max:
		if is_doubled(str(min)):
			print(min)
			answer = answer + int(min)
		min = min + 1

print('=====')
print(answer)