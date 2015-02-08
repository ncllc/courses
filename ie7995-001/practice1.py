# This script performs a simple minimization with constraints
# Find x that minimizes
#
#
from __future__ import print_function


import cplex
from cplex.exceptions import CplexError


my_obj      = [-5.0, -4.0, -6.0]
my_ub       = [cplex.infinity, cplex.infinity, cplex.infinity]
my_colnames = ["x1", "x2", "x3"]
my_rhs      = [20.0, 42.0, 30.0]
my_rownames = ["c1", "c2", "c3"]
my_sense    = "LLL"


# Creates the problem object, by calling the cplex ctor.
prob = cplex.Cplex()

# On the problem object, set the objective. In this case,
# set the minimize objective
prob.objective.set_sense(prob.objective.sense.minimize)

# Set the coefficients for the objective, alongwith respective upper bounds
# and define constraints
prob.variables.add(obj = my_obj, ub = my_ub, names = my_colnames)


# define constraints in rows
rows = [[["x1","x2","x3"],[1.0, -1.0, 1.0]],
        [["x1","x2","x3"],[3.0, 2.0, 4.0]],
        [["x1","x2","x3"],[3.0, 2.0, 0.0]]]

# add constraints to problem object, alongwith ineqalities
prob.linear_constraints.add(lin_expr = rows, senses = my_sense,
                            rhs = my_rhs, names = my_rownames)

# call cplex routine to solve problem
prob.solve()


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

prob.write("practice1.lp")
