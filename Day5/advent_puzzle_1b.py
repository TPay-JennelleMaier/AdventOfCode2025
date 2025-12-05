# day 5 puzzle 1
# https://adventofcode.com/2025/day/5

# you are given a copy of a database of ingredients and old they are
# there are IngredientIds
# the ranges are the ids that are Fresh (inclusive of min and max), ranges may overlap
# then a blank line
# then a list of available ids

# find out how many available ids are fresh


# first attempt was like sieve of eristothenes - keep a big array of True/False
# but that hit memory limits with the actual input
# so re-doing this to just check each range each time


import sys




def is_in_range(id, id_ranges):
	for id_range in id_ranges:
		if id >= id_range[0] and id <= id_range[1]:
			return True
	return False





input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)
lines = full_input.split('\n')


# get ranges
id_ranges = []
for line in lines:
	if line == '':
		break
	(min_id, max_id) = line.split('-')
	id_ranges.append( ( int(min_id), int(max_id) ) )

#print(id_ranges)
	


# count available+fresh ingredients
answer = 0
for line in lines:
	if '-' in line or line == '':
		continue
	id = int(line)
	if is_in_range(id, id_ranges):
		answer = answer + 1


print("=====")
print(answer)


