# advent of code - day 1 - puzzle 1
# https://adventofcode.com/2025/day/1
# collect stars by solving puzzles
#
# determine the safe combination
# you are given a series of rotation directions for the dial
# left is towards lower numbers, till 0 loops to 99
# right is towards higher numbers, till 99 loops to 0
# 11 + R8 => 19
# the dial starts at 50
# answer needed: the number of times the dial is left pointing at 0 after any rotation in the sequence

import sys




DIAL_MAX = 99
DIAL_MIN = 0

def rotate_dial(current_dial, instruction):
	is_left = instruction.startswith('L')
	rotations_to_apply = int(instruction[1:])
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
			
	return current_dial







input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

answer = 0 #count how many times dial stops at 0
dial = 50 #dial starts at 50

for line in full_input.split('\n'):
	#print(line)
	dial = rotate_dial(dial, line)
	if dial == 0:
		answer = answer + 1

print(answer)





