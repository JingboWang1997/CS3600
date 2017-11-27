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

        # Ui+1(s) = R(s)+y * maxaction_a[SUM(T(s,a,s') * Ui(s'))]

        for i in range(0, iterations):
            nextValues = util.Counter()  # temporary dto store values
            states = mdp.getStates()  # all states needed to be updates
            for state in states:
                reward = mdp.getReward(state, None, None)
                if mdp.isTerminal(state):
                    nextValues[state] = reward
                else:
                    actions = mdp.getPossibleActions(state)
                    bestActionValue = float("-inf")
                    for action in actions:
                        possibles = mdp.getTransitionStatesAndProbs(state, action)
                        sum = 0
                        for nextState, prob in possibles:
                            sum += (prob * self.values[nextState])
                        bestActionValue = max(bestActionValue, sum)
                    nextValues[state] = reward + (discount * bestActionValue)
            self.values = nextValues




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
        # Ui+1(s) = R(s)+y * maxaction_a[SUM(T(s,a,s') * Ui(s'))]
        # Q-value = R(s)+y * SUM(T(s,a,s') * Ui(s'))

        if self.mdp.isTerminal(state): # if terminal, return illegal
            return self.mdp.getReward(state, None, None)

        reward = self.mdp.getReward(state, None, None)
        y = self.discount
        possibles = self.mdp.getTransitionStatesAndProbs(state, action)

        sum = 0
        for nextState, prob in possibles:
            sum += (prob * self.values[nextState])
        return reward + (y * sum)



    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        # Ui+1(s) = R(s)+y * maxaction_a[SUM(T(s,a,s') * Ui(s'))]
        # pi* = maxaction_a[SUM(T(s,a,s') * Ui(s'))]

        if self.mdp.isTerminal(state): # if terminal, return illegal
            return None
        actions = self.mdp.getPossibleActions(state)

        bestAction = None
        maxValue = float("-inf")

        for action in actions:
            possibles = self.mdp.getTransitionStatesAndProbs(state, action)
            sum = 0
            for nextState, prob in possibles:
                sum += (prob * self.values[nextState])
            if (sum > maxValue):
                maxValue = sum
                bestAction = action
        return bestAction



    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
