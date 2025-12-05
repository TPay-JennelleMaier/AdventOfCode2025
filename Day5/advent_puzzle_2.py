# day 5 puzzle 2
# https://adventofcode.com/2025/day/5#part2

# now focus on just the id ranges of fresh ids
# just count the number of ids covered by any of the overlapping rangse

# i will try summing the overlapping ranges together, until only non-overlapping ranges are left


import sys



def is_in_range(id, id_range):
	return id >= id_range[0] and id <= id_range[1]




def ranges_overlap(range_a, range_b):
	if is_in_range(range_a[0], range_b):
		return True
	if is_in_range(range_a[1], range_b):
		return True
	if is_in_range(range_b[0], range_a):
		return True
	if is_in_range(range_b[1], range_a):
		return True
	return False



def sum_ranges(range_a, range_b):
	return ( min(range_a[0], range_b[0]), max(range_a[1], range_b[1]) )




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
	

# sum as many ranges together as possible
change_happened = True
while change_happened:
	change_happened = False
	#print("start again")
	i = 0
	while i < len(id_ranges) - 1:
		j = i + 1
		while j < len(id_ranges):
			#print("compare "+str(i)+" to "+str(j))
			if ranges_overlap(id_ranges[i], id_ranges[j]):
				id_ranges[i] = sum_ranges(id_ranges[i], id_ranges[j])
				id_ranges = id_ranges[:j] + id_ranges[j+1:]
				change_happened = True
			j = j + 1
		i = i + 1



print(id_ranges)


# count fresh ids
answer = 0
for id_range in id_ranges:
	answer = answer + (id_range[1] - id_range[0] + 1)


print("=====")
print(answer)




