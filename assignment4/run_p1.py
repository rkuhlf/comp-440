import util, submission


print('\nn-queens CSP example:')
csp = submission.create_nqueens_csp()
alg = submission.BacktrackingSearch()
alg.solve(csp)
print(('One of the optimal assignments:',  alg.optimalAssignment))
