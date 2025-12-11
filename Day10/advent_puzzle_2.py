# day 10 puzzle 2
# https://adventofcode.com/2025/day/10#part2

# input describes one machine per line
# indicator lights in [ ]
  # . = off and # = on and all lights on the machine start off
# button wiring schemetics (one or more) in ( ) with spaces between
  # pushing a button changes the state of indicator lights
  # 0 indicates first light index, and so on - the list of numbers is the list of lights that will toggle

# joltage requirements in { }
  # the buttons can also control the joltage levels
  # all joltage counters start at zero, and you want to configure it to match the input line
  # each time you push a button, the corrlated joltage value increases by 1

# find the fewest total button presses to configure all the joltages

# first round of just sample input took longer to complete than i'd like
# what can go faster?
  # the order of button clicks does not matter, so AAB == ABA == BAA
  # I could either uses sets...or I could say "you can only click a button at the same or larger index than you've last clicked" (nice!)
# yes, much faster on sample and still correct answer

# ok on actual input still need faster
  # i can check that with the remaining buttons it is still possible to click the buttons that need clicking
  # sample still passes
  # no, still taking too long on actual

# i could organize the buttons based on joltage 0th then 1st then 2nd, etc
  # stick to the buttons that affect 0th joltage until it is at the right value, then the buttons for 1st, etc
  # nope not helping speed
  # and really, there will still be lots of repeated AAB/ABA/BAA permutations here
    # commented this change out

# add in: order buttons largest to smallest, so the big-effect buttons get pruned out of the permutation tree as soon as possible

# that is still taking a while - machine 3 is up to 8million active permutations...18mill...51mill and 42GBmem...79mill
  # is this actually a depth-first search that looks like a breadth-first search? but if that's the case then i should be able to prune the tree faster
  # how else can i prune?
  # ok, i'm just stopping that run
# let's confirm the button ordering is working as intended
  # yes, confirmed on sample input and print statements

# ...long pause

# i see in actual 3th machine that index 4 and 7 always appear together, and that their target joltages are the same (which they'd have to be)
  # does this prune the tree at all?
  # i don't think that prunes the tree

# ok, now looking at pairs of joltage_indexes which appear together in buttons
# if, in the remaining rightward buttons, index A only appears when index B is also present, but they need diff number of additional clicks and A needs more than B
  # then that is another case where the tree can be pruned
  # this doesn't seem to me like it'd make much of a difference, but let's try it
	# PAUSE - I'm not even running my "if impossible" method! the return value is wrong!  trying with this part enabled first
	# ah! way faster already! whipped right through action 0 to 2 and is working on 3, now 4!  ok, going to let this one run
        # it is slowing down on 11th machine - up to 3mill permutations there...
	# 11th machine has some interesting properties, like 1vs7 and 6vs9
	# if there is only one button that has A without B, and A goal is higher than B goal, then answer must have that one button clicked X times...but this math is more detailed than I think I can cowboy-code after all this effort...can i simplify it?
  # 11th machine still going slow at 7mill permutations, so stopping that run to try this change
    # sample input passed
    # trying on actual now...reached 11th machine in maybe 2min...it /is/ changing the permutations counts from the last run, some a bit higher some a bit lower...but it doesn't feel like enough
  # commenting out this part again

"""
input for 11th machine
index: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
goal: 76,63,42,74,41,53,91,81,69,72
button: 1,2,3,5,6,7,8,9
button: 0,1,2,6,7,8,9
button: 0,1,3,5,7,8
button: 0,3,4,5,7,8
button: 4,5,6,7,8,9
button: 0,4,5,6,8
button: 0,3,4,6
button: 2,3,7
button: 0,6,9
button: 3,8,9
button: 6,9
button: 1

REORDERED
index: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
goal: 76,63,42,74,41,53,91,81,69,72
button: 0,3,4,6
button: 0,1,3,5,7,8
button: 0,1,2,6,7,8,9
button: 0,6,9
button: 0,3,4,5,7,8
button: 0,4,5,6,8
button: 1
button: 1,2,3,5,6,7,8,9
button: 2,3,7
button: 3,8,9
button: 4,5,6,7,8,9
button: 6,9
"""
# what if i sort the buttons so that all the 0 are first, then all the remaining 1s, then all the remaining 2s ?
  # ok, sample still runs fast and correct
  # trying actual - fast start, already in 4th machine - might be getting bogged down in 4th...yeah its no good for 4th
# trying another sort
"""
11th
goal: 76,63,42,74,41,53,91,81,69,72
button: 0,1,2,6,7,8,9
button: 0,1,3,5,7,8
button: 0,3,4,5,7,8
button: 0,3,4,6
button: 0,4,5,6,8
button: 0,6,9
button: 1,2,3,5,6,7,8,9
button: 1
button: 2,3,7
button: 3,8,9
button: 4,5,6,7,8,9
button: 6,9
"""
  # actual - slowing in 4th - still slow
  # ok, returning to first sort order - OH! hadn't realized 3th was that slow on first sort option...so sort makes a big diff and is diff for each machine
# trying different sorts on diff machines
  # 3th fast - 4th medium length - 8th took a moment - 10th took a moment - into 11th...ah but this is the same sort as used on 11th in the first place, and I know that will be too slow - so no progress on this part
  # well, no new ideas right now so just going to let it run while i take a break...30min later and 11th permutation count is finally dropping from 8mill to 5mill...still on 11th but permutations have dropped to 2mill...yay, we are at 32th! - still on 32th with 18mill permutations, oof - now at 30mill permmutations - now at 41mill permutations - now at 47mill...this is totally not going to finish any time reasonable, it will crash when i go to sleep and stop keeping the screen awake...ok, still no solution here...shutting it down on 32th with 61mill permutations




import sys


class Button:
	def __init__(self, config_term, button_index):
		config_term = config_term.replace('(','').replace(')','')
		self.joltage_indexes = [int(x) for x in config_term.split(',')]
		self.index = button_index
	
	def __str__(self):
		return "button: "+ ",".join([str(x) for x in self.joltage_indexes])
	
	def __repr__(self):
		return self.__str__()

		

class JoltageState:
	def __init__(self, initial_state):
		self.joltage_state = initial_state.copy()
		self.button_clicks = []

	def push_buttons(self, button_index, button):
		self.button_clicks.append(button_index)
		for joltage_index in button.joltage_indexes:
			self.joltage_state[joltage_index] = self.joltage_state[joltage_index] + 1
	
	def __str__(self):
		return "jolts: "+ ",".join([str(int(x)) for x in self.joltage_state])
	
	def __repr__(self):
		return self.__str__()

	def copy(self):
		result = JoltageState(self.joltage_state)
		result.button_clicks = self.button_clicks.copy()
		return result



class Machine:
	def __init__(self, config_line):
		# list of ints
		self.joltage_goal = [int(x) for x in config_line.split(' ')[-1].replace('{','').replace('}','').split(',')]
		self.joltages = [0] * len(self.joltage_goal)

		self.buttons = []
		for config_term in config_line.split(' '):
			if config_term[0] == '(':
				button_index = len(self.buttons)
				self.buttons.append(Button(config_term, button_index))
		if len([b for b in self.buttons if len(b.joltage_indexes) < 3]) > 1:
			# use first sort option
			self.buttons.sort(key=lambda b: len(b.joltage_indexes), reverse=True)
		else:
			# use third sort option
			self.buttons.sort(key=lambda b: "".join([str(b) for b in b.joltage_indexes])+"9999999999")

		#self.buttons.sort(key=lambda b: len(b.joltage_indexes), reverse=True) # sort longest to shortest sets
		#self.buttons.sort(key=lambda b: min(b.joltage_indexes)) # sort so zeros are first, then remaining ones, then remaining twos, etc
		#self.buttons.sort(key=lambda b: "".join([str(b) for b in b.joltage_indexes])+"9999999999") # sort so zeros are first, then remaining ones, then remaining twos, etc

		self.button_clicks = []

		self.buttons_by_joltage_index = [] # list of lists, ith is the list of buttons that can affect joltage_index "i"
		for i in range(len(self.joltage_goal)):
			result = []
			for button in self.buttons:
				if i in button.joltage_indexes:
					result.append(button)
			self.buttons_by_joltage_index.append(result)

		self.buttons_rightward_joltage_indexes = [] # list of lists, ith is the list of joltage indexes that appear in ith button plus all rightward buttons
		for i in range(len(self.buttons)):
			result = []
			for button in self.buttons[i:]:
				for joltage_index in button.joltage_indexes:
					result.append(joltage_index)
			self.buttons_rightward_joltage_indexes.append(result)

		"""
		self.button_rightward_a_means_b = [] # list of list of tuple(a,b), each increase for joltage a means an increase for joltage b
		for i in range(len(self.buttons)):
			result = []
			for a in range(len(self.joltage_goal)):
				buttons_with_a = [button for button in self.buttons if a in button.joltage_indexes]
				for b in range(len(self.joltage_goal)):
					if b == a:
						continue
					if len(buttons_with_a) == len([button for button in buttons_with_a if b in button.joltage_indexes]):
						result.append( (a,b) )
			self.button_rightward_a_means_b.append(result)
		"""

	
	def __str__(self):
		return "joltages: "+ ",".join([str(x) for x in self.joltages]) + "\ngoal: " + ",".join([str(x) for x in self.joltage_goal]) + "\n" + "\n".join([str(b) for b in self.buttons]) + "\n"
	
	def __repr__(self):
		return self.__str__()

	def calc_button_clicks(self, machine_index):
		self.button_clicks = [] # index of buttons to click
		# so, i want a breadth-first search of all possible permutations
		permutations = [] # list of LightsStates
		for i in range(len(self.buttons)):
			state = JoltageState(self.joltages)
			state.push_buttons(i, self.buttons[i])
			if state.joltage_state == self.joltage_goal:
				self.button_clicks = state.button_clicks
				return
			permutations.append(state)
		while True:
			print("working on machine "+str(machine_index)+" - "+str(len(permutations))+" permutations active")
			new_permutations = []
			for permutation in permutations:
				#print("".join([str(x) for x in permutation.button_clicks]))
				for i in range(len(self.buttons)):
					if i < permutation.button_clicks[-1]:
						continue # force button click ordering
					state = permutation.copy()
					state.push_buttons(i, self.buttons[i])
					if state.joltage_state == self.joltage_goal:
						self.button_clicks = state.button_clicks
						return
					if self.joltage_too_high(state):
						continue
					if self.joltage_goal_impossible(state):
						continue
					new_permutations.append(state)
			permutations = new_permutations
		#print(permutations)

	def joltage_too_high(self, joltage_state):
		# if any joltage is already too high a value, no need to keep pushing buttons on it
		for i in range(len(self.joltage_goal)):
			if joltage_state.joltage_state[i] > self.joltage_goal[i]:
				return True
		return False

	def get_first_joltage_index_too_low(self, joltage_state):
		for i in range(len(self.joltage_goal)):
			if joltage_state.joltage_state[i] < self.joltage_goal[i]:
				return i
		print("ERROR! A")

	def joltage_goal_impossible(self, joltage_state):
		# given the rule that it only works towards the right on buttons
		# if there are no more buttons remaining that can click the joltages that are still too low
		# then this permutation can be dropped
		for i in range(len(self.joltage_goal)):
			if joltage_state.joltage_state[i] < self.joltage_goal[i]:
				if self.buttons_dont_include_i(joltage_state.button_clicks[-1], i):
					return True
		"""
		# if all remaining buttons mean that when A increases then B will too
		# and A needs to increase more clicks than B at this point
		# then this permutation can be dropped
		# RISK this is dicey code - comment it out if any error is suspected
		for i in range(len(self.joltage_goal)):
			still_needed = self.joltage_goal[i] - joltage_state.joltage_state[i]
			if still_needed > 0:
				for a_means_b in [x for x in self.button_rightward_a_means_b[joltage_state.button_clicks[-1]] if x[0] == i]:
					still_needed_b = self.joltage_goal[a_means_b[1]] - joltage_state.joltage_state[a_means_b[1]]
					if still_needed > still_needed_b:
						return True
		"""
		return False

	def buttons_dont_include_i(self, leftmost_button_index, joltage_index):
		return not joltage_index in self.buttons_rightward_joltage_indexes[leftmost_button_index]
		"""
		while leftmost_button_index < len(self.buttons):
			if joltage_index in self.buttons[leftmost_button_index].joltage_indexes:
				return False
			leftmost_button_index = leftmost_button_index + 1
		return True
		"""
		



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

machines = []
for line in full_input.split('\n'):
	machines.append(Machine(line))
print(machines)


answer = 0
i = 0
for machine in machines:
	print("working on machine " + str(i))
	machine.calc_button_clicks(i)
	answer = answer + len(machine.button_clicks)
	i = i + 1
print("====")
print(answer)





