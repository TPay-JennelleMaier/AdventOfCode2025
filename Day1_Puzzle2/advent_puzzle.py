# advent of code - day 1 - puzzle 2
# https://adventofcode.com/2025/day/1#part2

# use password method 0x434C49434B
# meaning: count the number times the dial points at 0 at all (even when passing it)


import sys




DIAL_MAX = 99
DIAL_MIN = 0

# returns (current_dial, number_of_times_it_was_zero)
def rotate_dial(current_dial, instruction):
	is_left = instruction.startswith('L')
	rotations_to_apply = int(instruction[1:])
	zreo_count = 0
	while rotations_to_apply > 0:
		if is_left:
			current_dial = current_dial - 1
			if current_dial < DIAL_MIN:
				current_dial = DIAL_MAX
		else:
			current_dial = current_dial + 1
			if current_dial > DIAL_MAX:
				current_dial = DIAL_MIN
		rotations_to_apply = rotations_to_apply - 1
		if current_dial == 0:
			zreo_count = zreo_count + 1
			
	return (current_dial, zreo_count)







input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

dial = 50 #dial starts at 50
answer = 0 #count how many times dial touches 0

for line in full_input.split('\n'):
	#print(line)
	(new_dial, zero_count) = rotate_dial(dial, line)
	dial = new_dial
	answer = answer + zero_count

print(answer)

