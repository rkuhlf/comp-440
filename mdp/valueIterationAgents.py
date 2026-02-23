# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

import collections, math
import heapq

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):
            curr_V = util.Counter()
            for state in self.mdp.getStates():
                #if terminal, then value is 0
                if self.mdp.isTerminal(state):
                    curr_V[state] = 0
                else:
                    #Finding the expected value
                    actions = self.mdp.getPossibleActions(state)
                    if len(actions) == 0:
                        curr_V[state] = 0
                    else:
                        curr_max = float("-inf")
                        for action in actions:
                            q_value = self.computeQValueFromValues(state, action)
                            if q_value > curr_max:
                                curr_max = q_value
                        curr_V[state] = curr_max
            self.values = curr_V


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        result = 0.0
        for neighbor, prob in self.mdp.getTransitionStatesAndProbs(state, action):
            result += prob * (self.mdp.getReward(state, action, neighbor) + self.discount * self.values[neighbor])
        return result
    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None
        actions = self.mdp.getPossibleActions(state)
        if len(actions) == 0:
            return None
        curr_max = float("-inf")
        best_action = None
        for action in actions:
            curr_Q = self.computeQValueFromValues(state, action)
            if curr_Q > curr_max:
                curr_max = curr_Q
                best_action = action
        return best_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        # Compute predecessors.
        pred = collections.defaultdict(set)
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for neighbor, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob <= 0:
                        continue
                    pred[neighbor].add(state)
        
        heap = util.PriorityQueue()
        pendingDiff = util.Counter()
        for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
                continue
            diff = self.getUpdateDiff(state)
            heap.push(state, -abs(diff))
            pendingDiff[state] = diff
            
        for _ in range(self.iterations):
            if heap.isEmpty():
                return

            s = heap.pop()
            self.values[s] += pendingDiff[s]
            # print(self.values[s], pendingDiff[s])
            del pendingDiff[s]
            
            for p in pred[s]:
                diff = self.getUpdateDiff(p)
                if abs(diff) < self.theta:
                    continue
            
                heap.update(p, -abs(diff))
                if abs(pendingDiff[p]) < abs(diff):
                    pendingDiff[p] = diff
                
    def getUpdateDiff(self, state):
        highest_v = -math.inf
        for action in self.mdp.getPossibleActions(state):
            highest_v = max(self.computeQValueFromValues(state, action), highest_v)
        
        return highest_v - self.values[state]