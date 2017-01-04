# Constraint Satisfier
#
# Jake Wilson
# 12/30/16
#

import sys
import parser as parser_lib

class Problem:

    def __init__(self, definition):
        self.variables = []
        for v in definition[0]:
            self.variables.append((v, definition[2]))
        self.constraints = definition[1]
        # indices for the variable list of tuples
        self.NAME = 0
        self.DOMAIN = 1

        self.FAILURE = 1

    def complete(self, assignment):
        return len(self.variables) == len(assignment)

    def checkConstraints(self, assignment):
        for constraint in self.constraints:
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




if len(sys.argv) == 0:
    print "[ERROR] you must enter a constraint file."
    sys.exit(1)

parser = parser_lib.Parser()
problem = Problem(parser.parse(open(sys.argv[1])))
print backtrackingSearch(problem)
