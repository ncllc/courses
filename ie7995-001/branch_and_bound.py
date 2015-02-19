from __future__ import print_function
import cplex
import math
import argparse
import os
 

class SubProblem():
	# cplex_problem is the cplex representation of the problem generated from *.lp file
	def __init__(self, cplex_problem):  
		self.cplex_problem = cplex_problem
		# to keep track of each additional constraint under a subproblem
		# we are creating a dictionary (hash map)
		self.additional_constraints = {}

	def solve(self):
		# find all the 
		for i in self.additional_constraints.keys():
			(isLower, value) = 	self.additional_constraints[i]
			if isLower:
				self.cplex_problem.variables.set_lower_bounds(i, value)
			else:
				self.cplex_problem.variables.set_upper_bounds(i, value)
		print('solving with additional constraints', self.additional_constraints)
		print('lower', self.cplex_problem.variables.get_lower_bounds())
		print('upper', self.cplex_problem.variables.get_upper_bounds())

		# calling solve on the cplex object
		self.cplex_problem.solve()

		# retrieve staus from cplex object
		status = self.cplex_problem.solution.get_status()
		print(self.cplex_problem.solution.status[status])
		if status == self.cplex_problem.solution.status.unbounded:
		    print("Model is unbounded")
		    return False
		if status == self.cplex_problem.solution.status.infeasible:
		    print("Model is infeasible")
		    return False
		if status == self.cplex_problem.solution.status.infeasible_or_unbounded:
		    print("Model is infeasible or unbounded")
		    return False
		return True

	def get_objective_value(self):
		return self.cplex_problem.solution.get_objective_value()

	def get_values(self):
		return self.cplex_problem.solution.get_values()		

	# returns first non integral solution, alongwith 
	# it's index (0-indexed), and its corresponding integral floor
	# and ceiling values. In the case there are non-integrals
	# it returs null, implying that all variables are integrals.
	def find_first_non_integral(self):
		num_variables = self.cplex_problem.variables.get_num()
		x = self.cplex_problem.solution.get_values()
		print("[x of i's]", x)
		for i in range(num_variables):
			# Mod operator is used to check if 
			# the current solution is non-integral
			if x[i] % 1 > 0:
				floor = math.floor(x[i])
				ceil = math.ceil(x[i])
				return (i, x[i], floor, ceil)
		return  None




def main():
	parser = argparse.ArgumentParser(description="Run branch and bound")
	parser.add_argument('-i', '--input', help='location of input lp file')
	args = parser.parse_args()

	if not args.input:
		parser.print_help()
		return


	if not os.path.exists(args.input):
		print('Invalid path %s' % args.input)
		return

	# Read in the cplex file location
	cplex_file = args.input

	# Instantiate SubProblem, while passing into
	# ctor the cplex object from the file location
	# stored in cplex_file
	sub_problem = SubProblem(cplex.Cplex(cplex_file))

	# Creating an empty queue, this is modeled as 
	# a list. Queue has FIFO behavior
	queue = []

	# Enqueue initial problem
	queue.append(sub_problem)


	# global variables for lower and upper bounds of
	# Z
	z_min = None
	z_max = None

	# intermediate optimal solution
	candidate_solution = None


	# Iteration logic is based on exploration of
	# state space via breadth first search
	i = 0
	while(len(queue) != 0):
		i = i + 1
		print("-------------")
		print("Pass:", i)
		# dequeue problem from queue
		current_problem = queue.pop(0)

		# checks for feasibility and if not 
		# feasible fathoms and goes to top 
		# of the while-loop
		if not current_problem.solve():
			continue

		# find z at the subproblem
		objective_value = current_problem.get_objective_value()


		# for inital case of no value being present on
		# z_max, assign objective_value to z_max
		if z_max == None:
			z_max = objective_value

		# Fathom spaces where objective_value is less 
		# than z_min and goto top of while-loop
		if z_min and objective_value < z_min:
			continue

		# Branching decision on non integral solutions
		# are done by selecting the first non integral
		# solution.
		first_non_integral = current_problem.find_first_non_integral()

		print("[objective_value]", objective_value)
		# printing index of first_non_integral, the current solution value,
		# the upper bound and the lower bound respectively
		print("[index, non_integral_value, upper_bound, lower_bound]", first_non_integral)

		if not first_non_integral:
			print('found integral solution', (objective_value, current_problem.get_values()))
			if z_min == None or z_min < objective_value:
				z_min = objective_value
				candidate_solution = (objective_value, current_problem.get_values())
		else:
			sub_problem_floor = SubProblem(cplex.Cplex(cplex_file))
			sub_problem_ceil = SubProblem(cplex.Cplex(cplex_file))

			for variable_index, (isLower, value) in current_problem.additional_constraints.items():
				sub_problem_floor.additional_constraints[variable_index] = (isLower, value)
				sub_problem_ceil.additional_constraints[variable_index] = (isLower, value)
			
			variable_index, variable_value, floor, ceil = first_non_integral
			sub_problem_floor.additional_constraints[variable_index] = (False, floor)
			sub_problem_ceil.additional_constraints[variable_index] = (True, ceil)

			# Enqueue sub-problems into the queue
			queue.append(sub_problem_floor)
			queue.append(sub_problem_ceil)


	print('Solution', candidate_solution)
	print('Done')

if __name__ == "__main__":
    main()




