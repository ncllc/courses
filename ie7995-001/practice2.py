from __future__ import print_function
import cplex


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




prob = cplex.Cplex("practice2.lp")

prob.variables.set_upper_bounds(0, 1.0)
prob.variables.set_lower_bounds(1, 4.0)

#prob.variables.set_lower_bounds(0, 2.0)
prob.solve()

printSolution(prob)

status = prob.solution.get_status()
print(prob.solution.status[status])
if status == prob.solution.status.unbounded:
    print("Model is unbounded")
if status == prob.solution.status.infeasible:
    print("Model is infeasible")
if status == prob.solution.status.infeasible_or_unbounded:
    print("Model is infeasible or unbounded")



