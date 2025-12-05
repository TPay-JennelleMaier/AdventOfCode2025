# day 5 puzzle 1
# https://adventofcode.com/2025/day/5

# you are given a copy of a database of ingredients and old they are
# there are IngredientIds
# the ranges are the ids that are Fresh (inclusive of min and max), ranges may overlap
# then a blank line
# then a list of available ids

# find out how many available ids are fresh



import sys




def get_max_id_in_range(lines):
	max_id_in_range = 0
	for line in lines:
		if line == '':
			break
		max_id = int(line.split('-')[1])
		if max_id > max_id_in_range:
			max_id_in_range = max_id
	return max_id_in_range




input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)
lines = full_input.split('\n')

max_id_in_range = get_max_id_in_range(lines)

# determine freshness ranges
id_freshness = [False] * (max_id_in_range + 1)
len_id_freshness = len(id_freshness)
for line in lines:
	if line == '':
		break
	(min_id, max_id) = line.split('-')
	i = int(min_id)
	j = int(max_id)
	while i <= j:
		id_freshness[i] = True
		i = i + 1
	
#print(id_freshness)


# count available+fresh ingredients
answer = 0
for line in lines:
	if '-' in line or line == '':
		continue
	id = int(line)
	if id < len_id_freshness and id_freshness[id]:
		answer = answer + 1


print("=====")
print(answer)


