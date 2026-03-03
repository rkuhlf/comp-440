#!/usr/bin/env python
"""
Grader for template assignment
Optionally run as grader.py [basic|all] to run a subset of tests
"""

import random

import graderUtil
import util
import collections
import copy
grader = graderUtil.Grader()
submission = grader.load('submission')


############################################################
# Problem 4.1: N-Queens

def test1a_1():
    nQueensSolver = submission.BacktrackingSearch()
    nQueensSolver.solve(submission.create_nqueens_csp(8))
    grader.requireIsEqual(1.0, nQueensSolver.optimalWeight)
    grader.requireIsEqual(92, nQueensSolver.numOptimalAssignments)
    grader.requireIsEqual(2057, nQueensSolver.numOperations)

grader.addBasicPart('4.1-1-basic', test1a_1, 2, maxSeconds=1, description="Basic test for create_nqueens_csp for n=8")

def test1a_2():
    nQueensSolver = submission.BacktrackingSearch()
    nQueensSolver.solve(submission.create_nqueens_csp(3))

grader.addHiddenPart('4.1-2-hidden', test1a_2, 1, maxSeconds=1, description="Test create_nqueens_csp with n=3")

def test1a_3():
    nQueensSolver = submission.BacktrackingSearch()
    nQueensSolver.solve(submission.create_nqueens_csp(4))

    nQueensSolver = submission.BacktrackingSearch()
    nQueensSolver.solve(submission.create_nqueens_csp(7))

grader.addHiddenPart('4.1-3-hidden', test1a_3, 1, maxSeconds=1, description="Test create_nqueens_csp with different n")

############################################################
# Problem 4.2: Most constrained variable


def test1b_1():
    mcvSolver = submission.BacktrackingSearch()
    mcvSolver.solve(submission.create_nqueens_csp(8), mcv = True)
    grader.requireIsEqual(1.0, mcvSolver.optimalWeight)
    grader.requireIsEqual(92, mcvSolver.numOptimalAssignments)
    grader.requireIsEqual(1361, mcvSolver.numOperations)

grader.addBasicPart('4.2-1-basic', test1b_1, 1, maxSeconds=1, description="Basic test for MCV with n-queens CSP")

def test1b_2():
    mcvSolver = submission.BacktrackingSearch()
    # We will use our implementation of n-queens csp
    mcvSolver.solve(submission.create_nqueens_csp(6), mcv = True)

grader.addHiddenPart('4.2-2-hidden', test1b_2, 1, maxSeconds=1, description="Test for MCV with n-queens CSP")

def test1b_3():
    mcvSolver = submission.BacktrackingSearch()
    mcvSolver.solve(util.create_map_coloring_csp(), mcv = True)

grader.addHiddenPart('4.2-3-hidden', test1b_3, 2, maxSeconds=1, description="Test MCV with different CSPs")

############################################################
# Problem 4.3: Arc consistency

def test1c_1():
    acSolver = submission.BacktrackingSearch()
    acSolver.solve(submission.create_nqueens_csp(8), ac3 = True)
    grader.requireIsEqual(1.0, acSolver.optimalWeight)
    grader.requireIsEqual(92, acSolver.numOptimalAssignments)
    # Removing the test below in all subparts due to ambiguity in number of
    # operations based on ordering of list elements.
    # grader.requireIsEqual(21, acSolver.firstAssignmentNumOperations)
    grader.requireIsEqual(769, acSolver.numOperations)

grader.addBasicPart('4.3-1-basic', test1c_1, 1, maxSeconds=1, description="Basic test for AC-3 with n-queens CSP")

def test1c_2():
    acSolver = submission.BacktrackingSearch()
    acSolver.solve(util.create_map_coloring_csp(), ac3 = True)

grader.addHiddenPart('4.3-2-hidden', test1c_2, 2, maxSeconds=1, description="Test AC-3 for map coloring CSP")

def test1c_3():
    acSolver = submission.BacktrackingSearch()
    acSolver.solve(submission.create_nqueens_csp(8), mcv = True, ac3 = True)

grader.addHiddenPart('4.3-3-hidden', test1c_3, 1, maxSeconds=1, description="Test MCV+AC-3 for n-queens CSP with n=8")

def test1c_4():
    acSolver = submission.BacktrackingSearch()
    acSolver.solve(submission.create_nqueens_csp(7), mcv = True, ac3 = True)

grader.addHiddenPart('4.3-4-hidden', test1c_4, 2, maxSeconds=1, description="Test MCV+AC-3 for n-queens CSP with n=7")

def test1c_5():
    acSolver = submission.BacktrackingSearch()
    acSolver.solve(util.create_map_coloring_csp(), mcv = True, ac3 = True)

grader.addHiddenPart('4.3-5-hidden', test1c_5, 2, maxSeconds=1, description="Test MCV+AC-3 for map coloring CSP")



############################################################
# Problem 4.5 and 4.6: add quarter constraints and unit load

def verify_schedule(bulletin, profile, schedule, checkUnits = True):
    """
    Returns true if the schedule satisifies all requirements given by the profile.
    """
    goodSchedule = True
    all_courses_taking = dict((s[1], s[0]) for s in schedule)

    # No course can be taken twice.
    goodSchedule *= len(all_courses_taking) == len(schedule)
    if not goodSchedule:
        print ('course repeated')
        return False

    # Each course must be offered in that quarter.
    goodSchedule *= all(bulletin.courses[s[1]].is_offered_in(s[0]) for s in schedule)
    if not goodSchedule:
        print ('course not offered')
        return False

    # If specified, only take the course at the requested time.
    for req in profile.requests:
        if len(req.quarters) == 0: continue
        goodSchedule *= all([s[0] in req.quarters for s in schedule if s[1] in req.cids])
    if not goodSchedule:
        print ('course taken at wrong time')
        return False

    # If a request has multiple courses, at most one is chosen.
    for req in profile.requests:
        if len(req.cids) == 1: continue
        goodSchedule *= len([s for s in schedule if s[1] in req.cids]) <= 1
    if not goodSchedule:
        print ('more than one exclusive group of courses is taken')
        return False

    # Must take a course after the prereqs
    for req in profile.requests:
        if len(req.prereqs) == 0: continue
        cids = [s for s in schedule if s[1] in req.cids] # either empty or 1 element
        if len(cids) == 0: continue
        quarter, cid, units = cids[0]
        for prereq in req.prereqs:
            if prereq in profile.taking:
                goodSchedule *= prereq in all_courses_taking
                if not goodSchedule:
                    print ('not all prereqs are taken')
                    return False
                goodSchedule *= profile.quarters.index(quarter) > \
                    profile.quarters.index(all_courses_taking[prereq])
    if not goodSchedule:
        print ('course is taken before prereq')
        return False

    if not checkUnits: return goodSchedule
    # Check for unit loads
    unitCounters = collections.Counter()
    for quarter, c, units in schedule:
        unitCounters[quarter] += units
    goodSchedule *= all(profile.minUnits <= u and u <= profile.maxUnits \
        for k, u in unitCounters.items())
    if not goodSchedule:
        print ('unit count out of bound for quarter')
        return False

    return goodSchedule

# Load all courses.
bulletin = util.CourseBulletin('courses.json')

############################################################
# Problem 4.5: Quarter specification

def test3a_1():
    profile = util.Profile(bulletin, 'profile3a.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_quarter_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp)

    # Verify correctness.
    grader.requireIsEqual(3, alg.numOptimalAssignments)
    sol = util.extract_course_scheduling_solution(profile, alg.optimalAssignment)
    for assignment in alg.allAssignments:
        sol = util.extract_course_scheduling_solution(profile, assignment)
        grader.requireIsTrue(verify_schedule(bulletin, profile, sol, False))

grader.addBasicPart('4.5a-1-basic', test3a_1, 2, maxSeconds=4, description="Basic test for add_quarter_constraints")

def test3a_2():
    profile = util.Profile(bulletin, 'profile3a1.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_quarter_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp)

    # Verify correctness.

grader.addHiddenPart('4.5a-2-hidden', test3a_2, 2, maxSeconds=3, description="Test add_quarter_constraints with different profiles")

def test3a_3():
    profile = util.Profile(bulletin, 'profile3a2.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_quarter_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp)

    # Verify correctness.

grader.addHiddenPart('4.5a-3-hidden', test3a_3, 1, maxSeconds=3, description="Test add_quarter_constraints with no quarter specified")

############################################################
# Problem 4.6: Unit load

def test3b_1():
    profile = util.Profile(bulletin, 'profile3b.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_unit_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp)

    # Verify correctness.
    grader.requireIsEqual(15, alg.numOptimalAssignments)
    for assignment in alg.allAssignments:
        sol = util.extract_course_scheduling_solution(profile, assignment)
        grader.requireIsTrue(verify_schedule(bulletin, profile, sol))

grader.addBasicPart('4.6b-1-basic', test3b_1, 2, maxSeconds=7, description="Basic test for add_unit_constraints")

def test3b_2():
    profile = util.Profile(bulletin, 'profile3b1.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_unit_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp)

    # Verify correctness.

grader.addHiddenPart('4.6b-2-hidden', test3b_2, 3, maxSeconds=3, description="Test add_unit_constraints with different profiles")

def test3b_3():
    profile = util.Profile(bulletin, 'profile3b2.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_all_additional_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp)

    # Verify correctness.

grader.addHiddenPart('4.6b-3-hidden', test3b_3, 1, maxSeconds=4, description="Test unsatisfiable scheduling")

def test3b_4():
    profile = util.Profile(bulletin, 'profile3b3.txt')
    cspConstructor = submission.SchedulingCSPConstructor(bulletin, copy.deepcopy(profile))
    csp = cspConstructor.get_basic_csp()
    cspConstructor.add_all_additional_constraints(csp)
    alg = submission.BacktrackingSearch()
    alg.solve(csp, mcv = True, ac3 = True)

    # Verify correctness.

grader.addHiddenPart('4.6b-4-hidden', test3b_4, 3, maxSeconds=25, description="Test MVC+AC-3+all additional constraints")


grader.grade()
