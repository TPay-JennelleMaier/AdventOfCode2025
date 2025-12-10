# day 10 puzzle 1
# https://adventofcode.com/2025/day/10

# input describes one machine per line
# indicator lights in [ ]
  # . = off and # = on and all lights on the machine start off
# button wiring schemetics (one or more) in ( ) with spaces between
  # pushing a button changes the state of indicator lights
  # 0 indicates first light index, and so on - the list of numbers is the list of lights that will toggle
# joltage requirements in { }
  # can be ignored for now

# determine the fewest number of button clicks needed to get all the indicator lights correct
# the answer is the total number of button clicks used for all the machines



import sys


class Button:
	def __init__(self, config_term):
		config_term = config_term.replace('(','').replace(')','')
		self.light_indexes = [int(x) for x in config_term.split(',')]
	
	def __str__(self):
		return "button: "+ ",".join([str(x) for x in self.light_indexes])
	
	def __repr__(self):
		return self.__str__()

		

class LightsState:
	def __init__(self, initial_state):
		self.lights_state = initial_state.copy()
		self.button_clicks = []

	def push_buttons(self, button_index, button):
		self.button_clicks.append(button_index)
		for light_index in button.light_indexes:
			self.lights_state[light_index] = not self.lights_state[light_index]
	
	def __str__(self):
		return "lights: "+ ",".join([str(int(x)) for x in self.lights_state])
	
	def __repr__(self):
		return self.__str__()

	def copy(self):
		result = LightsState(self.lights_state)
		result.button_clicks = self.button_clicks.copy()
		return result



class Machine:
	def __init__(self, config_line):
		# list of booleans
		self.lights_goal = [x == '#' for x in config_line.split(' ')[0].replace('[','').replace(']','')]
		self.lights = [False] * len(self.lights_goal)

		self.buttons = []
		for config_term in config_line.split(' '):
			if config_term[0] == '(':
				self.buttons.append(Button(config_term))
	
	def __str__(self):
		return "lights: "+ ",".join([str(int(x)) for x in self.lights]) + "\ngoal: " + ",".join([str(int(x)) for x in self.lights_goal]) + "\n" + "\n".join([str(b) for b in self.buttons]) + "\n"
	
	def __repr__(self):
		return self.__str__()

	def calc_button_clicks(self):
		self.button_clicks = [] # index of buttons to click
		# so, i want a breadth-first search of all possible permutations
		permutations = [] # list of LightsStates
		for i in range(len(self.buttons)):
			state = LightsState(self.lights)
			state.push_buttons(i, self.buttons[i])
			if state.lights_state == self.lights_goal:
				self.button_clicks = state.button_clicks
				return
			permutations.append(state)
		while True:
			new_permutations = []
			for permutation in permutations:
				for i in range(len(self.buttons)):
					state = permutation.copy()
					state.push_buttons(i, self.buttons[i])
					if state.lights_state == self.lights_goal:
						self.button_clicks = state.button_clicks
						return
					new_permutations.append(state)
			permutations = new_permutations
		#print(permutations)
		



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




