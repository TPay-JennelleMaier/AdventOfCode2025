# day 2 puzzle 2
# https://adventofcode.com/2025/day/2#part2
#
# in addition to those invalid ids, ids are also invalid if they are made up of repeated segments of numbers for any number of repititions 2 and over
# ex: 55 6464 123123 but also 123123123 12121212 111111

import sys
import re


def is_multipled(text):
	length = len(text)
	divisor = 2
	while divisor <= length:
		if length%divisor == 0:
			index = int(length/divisor)
			unit = text[:index]
			if text == (str(unit) * divisor):
				return True
		divisor = divisor + 1
	return False



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
		if is_multipled(str(min)):
			print(min)
			answer = answer + int(min)
		min = min + 1

print('=====')
print(answer)