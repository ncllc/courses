from __future__ import print_function
import cplex
import math

def printSolution(prob):
	numrows = prob.linear_constraints.get_num()
	numcols = prob.variables.get_num()
	print()
	# solution.get_status() returns an integer code
	print("Solution status = " , prob.solution.get_status(), ":", end=' ')
	# the following line prints the corresponding string
	print(prob.solution.status[prob.solution.get_status()])
	print("Solution value  = ", prob.solution.get_objective_value())
	slack = prob.solution.get_linear_slacks()
	pi    = prob.solution.get_dual_values()
	x     = prob.solution.get_values()
	dj    = prob.solution.get_reduced_costs()
	for i in range(numrows):
	    print("Row %d:  Slack = %10f  Pi = %10f" % (i, slack[i], pi[i]))
	for j in range(numcols):
	    print("Column %d:  Value = %10f Reduced cost = %10f" % (j, x[j], dj[j]))




class SubProblem():
	def __init__(self, cplex_problem):
		self.cplex_problem = cplex_problem
		self.additional_constraints = {}

	def add_additional_contraints(self, variable_index, isLower, value):
		self.additional_constraints[variable_index] = (isLower, value)

	def solve(self):
		num_variables = self.cplex_problem.variables.get_num()
		for i in range(num_variables):
			self.cplex_problem.variables.set_lower_bounds(i, 0.0)
			self.cplex_problem.variables.set_upper_bounds(i, cplex.infinity)

			if i in self.additional_constraints:
				(isLower, value) = 	self.additional_constraints[i]
				if isLower:
					self.cplex_problem.variables.set_lower_bounds(i, value)
				else:
					self.cplex_problem.variables.set_upper_bounds(i, value)
		print('solving with additional constraints', self.additional_constraints)
		print('lower', self.cplex_problem.variables.get_lower_bounds())
		print('upper', self.cplex_problem.variables.get_upper_bounds())

		try:
			self.cplex_problem.solve()
		except:
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
			if z_min == None or z_min < objective_value:
				z_min = objective_value
				candidate_solution = (objective_value, current_problem.get_values())
		else:
			variable_index, variable_value, floor, ceil = first_non_integral
			sub_problem_floor = SubProblem(current_problem.cplex_problem)
			sub_problem_ceil = SubProblem(current_problem.cplex_problem)

			for variable_index, (isLower, value) in current_problem.additional_constraints.items(): 
				sub_problem_floor.add_additional_contraints(variable_index, isLower, value)
				sub_problem_ceil.add_additional_contraints(variable_index, isLower, value)

			sub_problem_floor.add_additional_contraints(variable_index, False, floor)
			sub_problem_ceil.add_additional_contraints(variable_index, True, ceil)


			queue.append(sub_problem_floor)
			queue.append(sub_problem_ceil)


	print(candidate_solution)
	print('Done')

if __name__ == "__main__":
    main()




