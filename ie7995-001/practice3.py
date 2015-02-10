from __future__ import print_function
import cplex
import math

 

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


		self.cplex_problem.solve()

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

	def find_first_non_integral(self):
		num_variables = self.cplex_problem.variables.get_num()
		x = self.cplex_problem.solution.get_values()
		for i in range(num_variables):
			if x[i] % 1 > 0:
				floor = math.floor(x[i])
				ceil = math.ceil(x[i])
				print(x, floor, ceil)
				return (i, x[i], floor, ceil)
		return  None




def main():
    
	sub_problem = SubProblem(cplex.Cplex("practice3.lp"))
	queue = []
	queue.append(sub_problem)

	z_min = None
	z_max = None
	candidate_solution = None


	while(len(queue) != 0):
		#raw_input("Please press 'enter' to iterate")
		current_problem = queue.pop(0)

		# checks for feasibility
		if not current_problem.solve():
			continue

		objective_value = current_problem.get_objective_value()


		if z_max == None:
			z_max = objective_value

		first_non_integral = current_problem.find_first_non_integral()

		print(objective_value)
		print(first_non_integral)

		# Fathom spaces where objective_value is less than z_min
		if z_min and objective_value < z_min:
			continue

		if not first_non_integral:
			print('found integral solution', (objective_value, current_problem.get_values()))
			if z_min == None or z_min < objective_value:
				z_min = objective_value
				candidate_solution = (objective_value, current_problem.get_values())
		else:
			sub_problem_floor = SubProblem(cplex.Cplex("practice3.lp"))
			sub_problem_ceil = SubProblem(cplex.Cplex("practice3.lp"))

			for variable_index, (isLower, value) in current_problem.additional_constraints.items():
				sub_problem_floor.additional_constraints[variable_index] = (isLower, value)
				sub_problem_ceil.additional_constraints[variable_index] = (isLower, value)
			
			variable_index, variable_value, floor, ceil = first_non_integral
			sub_problem_floor.additional_constraints[variable_index] = (False, floor)
			sub_problem_ceil.additional_constraints[variable_index] = (True, ceil)


			queue.append(sub_problem_floor)
			queue.append(sub_problem_ceil)


	print('Solution', candidate_solution)
	print('Done')

if __name__ == "__main__":
    main()




