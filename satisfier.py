# Constraint Satisfier
#
# Jake Wilson
# 12/30/16
#

class Problem:

    def __init__(self, variables=[], constraints=[]):
        self.variables = variables
        self.constraints = constraints
        # indices for the variable list of tuples
        self.NAME = 0
        self.DOMAIN = 1

        self.FAILURE = 1

    def complete(self, assignment):
        return len(self.variables) == len(assignment)

    def checkConstraints(self, assignment):
        for constraint in constraints:
            try:
                if not constraint(assignment):
                    return False
            except KeyError:
                continue

        return True


def getNextVar(problem, assignment):
    """ For now, just take the next variable from the list """
    return problem.variables[len(assignment)]

def backtrackingSearch(problem):
    return recBacktrackingSearch(problem, {})

def recBacktrackingSearch(problem, assignment):
    if problem.complete(assignment): return assignment
    var = getNextVar(problem, assignment)
    for val in var[problem.DOMAIN]:
        assignment[var[problem.NAME]] = val
        if problem.checkConstraints(assignment):
            res = recBacktrackingSearch(problem, assignment)
            if res != problem.FAILURE:
                return res
            
    return problem.FAILURE

variables = [('FL', set(['r', 'b', 'g'])), ('GA', set(['r', 'b', 'g'])), ('AL', set(['r', 'b', 'g']))]
constraints = [lambda a: a['FL'] != a['GA'], lambda a: a['FL'] != a['AL'], lambda a: a['GA'] != a['AL']]
problem = Problem(variables, constraints)
print backtrackingSearch(problem)
