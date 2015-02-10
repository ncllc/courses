from __future__ import print_function
import cplex
import argparse
import os



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


def main():
    parser = argparse.ArgumentParser(description="Run relaxed lp")
    parser.add_argument('-i', '--input', help='location of input lp file')

    args = parser.parse_args()

    if not args.input:
        parser.print_help()
        return

    if not os.path.exists(args.input):
        print 'Invalid path %s' % args.input
        return
        
	prob = cplex.Cplex(args.input)


	prob.solve()
	print('here')
	printSolution(prob)

	status = prob.solution.get_status()
	print(prob.solution.status[status])
	if status == prob.solution.status.unbounded:
	    print("Model is unbounded")
	if status == prob.solution.status.infeasible:
	    print("Model is infeasible")
	if status == prob.solution.status.infeasible_or_unbounded:
	    print("Model is infeasible or unbounded")


if __name__ == "__main__":
    main()


