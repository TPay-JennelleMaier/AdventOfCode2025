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

# taking a whole new approach in this new file





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


class ButtonSet:
	def __init__(self, joltage_goal, button_indexes, all_buttons):
		self.button_indexes = button_indexes
		self.buttons = [b for b in all_buttons if b.index in button_indexes]
		self.joltage_goal = joltage_goal
	
	def __str__(self):
		return "button set: joltage "+str(self.joltage_goal) + " = " + " + ".join(["button-"+str(x) for x in self.button_indexes])
	
	def __repr__(self):
		return self.__str__()

		

class Permutation:
	def __init__(self, initial_state):
		# same length as Machine.buttons
		# each element is the number of times this button was clicked
		# None means not determined yet
		self.current_state = initial_state.copy()

	def __str__(self):
		return "button clicks: "+ ",".join([str(x) for x in self.current_state])
	
	def __repr__(self):
		return self.__str__()



class Machine:
	def __init__(self, config_line):
		# list of ints
		self.joltage_goals = [int(x) for x in config_line.split(' ')[-1].replace('{','').replace('}','').split(',')]

		# list of Buttons
		self.buttons = []
		for config_term in config_line.split(' '):
			if config_term[0] == '(':
				button_index = len(self.buttons)
				self.buttons.append(Button(config_term, button_index))


		# list of ButtonSets
		# index matches joltage_goal index - these are the buttons that affect the ith joltage goal
		self.button_sets = []
		for i in range(len(self.joltage_goals)):
			button_indexes = [b.index for b in self.buttons if i in b.joltage_indexes]
			button_set = ButtonSet(self.joltage_goals[i], button_indexes, self.buttons)
			self.button_sets.append(button_set)

		self.shortest_permutation = None
		self.min_button_clicks = None

		self.cache_x_ints_sum_to_y = {} # dict key=(x,y) value=list of tuples

	
	def __str__(self):
		return "joltage goals: " + ",".join([str(x) for x in self.joltage_goals]) + "\n" + "\n".join([str(b) for b in self.buttons]) + "\n" + "\n".join([str(b) for b in self.button_sets]) + "\n"
	
	def __repr__(self):
		return self.__str__()

	def calc_button_clicks(self, machine_index):
		button_sets_todo = self.button_sets.copy()
		button_sets_todo.sort(key=lambda button_set: len(button_set.button_indexes)) #shortest to longest
		permutations = [ Permutation([None]*len(self.buttons)) ] # init with one empty permutation
		while len(button_sets_todo) > 0:
			# not sorting the button sets by anything yet, let's see if it matters
			next_button_set = button_sets_todo[0]
			button_sets_todo.remove(next_button_set)
			
			#print("next button set:"+str(next_button_set))

			next_permutations = []
			for p in permutations:
				next_permutations.extend( self.apply_button_set_to_permutation(p, next_button_set) )
			permutations = next_permutations
			print("machine: "+str(machine_index)+" permutation count: "+str(len(permutations)))
			#print(permutations)

		permutations.sort(key=lambda p: sum(p.current_state))
		self.shortest_permutation = permutations[0]
		print("shortest permutation: "+str(self.shortest_permutation))
		self.min_button_clicks = sum(self.shortest_permutation.current_state)

		print("machine "+str(machine_index)+" needed "+str(self.min_button_clicks)+" button clicks")

	# returns a list of new permutations
	def apply_button_set_to_permutation(self, permutation, button_set):
		# if a number is already set, it cannot be changed
		# i care about...the joltage goal of this button set, with its list of button_indexes...and the permutation.current_state uses button_indexes too
		remaining_joltage_goal = button_set.joltage_goal
		remaining_button_indexes = button_set.button_indexes.copy()
		for i in range(len(permutation.current_state)): #these are button_indexes
			if permutation.current_state[i] != None and i in remaining_button_indexes:
				remaining_joltage_goal = remaining_joltage_goal - permutation.current_state[i]
				remaining_button_indexes.remove(i)
		#print("remaining joltage goal: "+str(remaining_joltage_goal))
		#print(remaining_button_indexes)
		if remaining_joltage_goal < 0: # dead end, over joltage goal, invalid permutation
			return []
		if remaining_joltage_goal == 0:
			for i in remaining_button_indexes: # finished with this button set
				permutation.current_state[i] = 0
			return [ permutation ]
		if len(remaining_button_indexes) == 0:  # dead end, can't reach joltage goal, invalid permutation
			return []

		# build new permutations based on possible uses of the remaining_button_indexes
		# needs to sum to remaining_joltage_goal - how many ways for x ints to sum to y?
		x_ints_sum_to_y = self.how_x_ints_sum_to_y(len(remaining_button_indexes), remaining_joltage_goal)
		new_permutations = []
		for x_y_result in x_ints_sum_to_y:
			new_permutation = Permutation(permutation.current_state)
			for i in range(len(x_y_result)):
				new_permutation.current_state[remaining_button_indexes[i]] = x_y_result[i]
			new_permutations.append(new_permutation)
		#print("new permutations")
		#print(new_permutations)
		return new_permutations

	# returns a list of tuples - each tuple is one way for x ints to sum to y
	def how_x_ints_sum_to_y(self, x, y):
		# check cache
		if (x,y) in self.cache_x_ints_sum_to_y:
			#print("used cache for x="+str(x)+", y="+str(y))
			#print(self.cache_x_ints_sum_to_y[(x,y)])
			return self.cache_x_ints_sum_to_y[(x,y)]

		# find permutations
		results = []
		if x == 1:
			results.append( (y,) )
		else:
			for i in range(y+1):
				sub_results = self.how_x_ints_sum_to_y(x-1, y-i)
				#print("sub_results")
				#print(sub_results)
				for sub_result in sub_results:
					results.append( (i,)+sub_result )
		

		# update cache
		#print("set cache for x="+str(x)+", y="+str(y))
		#print(results)
		self.cache_x_ints_sum_to_y[(x,y)] = results

		return results

		



input_filename = sys.argv[1]
f = open(input_filename, "r")
full_input = f.read()
f.close()

print(full_input)

machines = []
for line in full_input.split('\n'):
	machines.append(Machine(line))
#print(machines)

answer = 0
i = 0
for machine in machines:
	print("working on machine " + str(i))
	machine.calc_button_clicks(i)
	answer = answer + machine.min_button_clicks
	i = i + 1
print("====")
print(answer)





