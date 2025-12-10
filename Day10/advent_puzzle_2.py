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
		self.button_clicks = []

		self.buttons_by_joltage_index = [] # list of lists, ith is the list of buttons that can affect joltage_index "i"
		for i in range(len(self.joltage_goal)):
			result = []
			for button in self.buttons:
				if i in button.joltage_indexes:
					result.append(button)
			self.buttons_by_joltage_index.append(result)
	
	def __str__(self):
		return "joltages: "+ ",".join([str(x) for x in self.joltages]) + "\ngoal: " + ",".join([str(x) for x in self.joltage_goal]) + "\n" + "\n".join([str(b) for b in self.buttons]) + "\n"
	
	def __repr__(self):
		return self.__str__()

	def calc_button_clicks(self):
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
			new_permutations = []
			for permutation in permutations:
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
				"""
				current_joltage_index = self.get_first_joltage_index_too_low(permutation)
				buttons_for_joltage_index = self.buttons_by_joltage_index[current_joltage_index]
				for button in buttons_for_joltage_index:
					state = permutation.copy()
					state.push_buttons(button.index, button)
					if state.joltage_state == self.joltage_goal:
						self.button_clicks = state.button_clicks
						return
					if self.joltage_too_high(state):
						continue
					if self.joltage_goal_impossible(state):
						continue
					new_permutations.append(state)
				"""
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
					return False
		return False

	def buttons_dont_include_i(self, leftmost_button_index, joltage_index):
		while leftmost_button_index < len(self.buttons):
			if joltage_index in self.buttons[leftmost_button_index].joltage_indexes:
				return False
			leftmost_button_index = leftmost_button_index + 1
		return True
		



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

#print(full_input)

machines = []
for line in full_input.split('\n'):
	machines.append(Machine(line))
#print(machines)


answer = 0
i = 0
for machine in machines:
	print("working on machine " + str(i))
	machine.calc_button_clicks()
	answer = answer + len(machine.button_clicks)
	i = i + 1
print("====")
print(answer)




