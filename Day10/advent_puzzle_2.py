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


import sys


class Button:
	def __init__(self, config_term):
		config_term = config_term.replace('(','').replace(')','')
		self.joltage_indexes = [int(x) for x in config_term.split(',')]
	
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
				self.buttons.append(Button(config_term))
		self.button_clicks = []
	
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
					state = permutation.copy()
					state.push_buttons(i, self.buttons[i])
					if state.joltage_state == self.joltage_goal:
						self.button_clicks = state.button_clicks
						return
					if self.joltage_too_high(state):
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
for machine in machines:
	machine.calc_button_clicks()
	answer = answer + len(machine.button_clicks)
print("====")
print(answer)




