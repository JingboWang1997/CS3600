# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

# check

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        # type: (object) -> object
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    # parents is a DICTIONARY storing the trace-back relationships
    # explore is a STACK
    # current is a tuple with the state (coordinate) and the action
    # found indicates if the goal is found
    parents = {}
    visited = []
    explore = util.Stack()
    actions = []
    current = (problem.getStartState(), None)
    explore.push(current)
    found = False
    # keep looping until either
    # the explore STACK is empty (goal is not reachable)
    # the goal is found
    while not explore.isEmpty() and not found:
        current = explore.pop()
        # this WHILE checks if the node out of the stack is already visited
        # if it is, ignore it and pop next
        while current[0] in visited:
            current = explore.pop()
        visited.append(current[0])
        neighbors = problem.getSuccessors(current[0])
        # looping through the neighbors
        for (state, action, cost) in neighbors:
            if state not in visited:
                neighbor = (state, action)
                explore.push(neighbor)
                parents[neighbor] = current
                # if the goal is found, terminate early
                if problem.isGoalState(state):
                    current = explore.pop()
                    found = True
                    break
    # if terminated on FOUND
    if found:
        # trace back and store the actions
        # current actions are ordered reversely
        while (current[0] != problem.getStartState()):
            actions.append(current[1])
            current = parents[current]
    # return a reversed list of actions
    return actions[::-1]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    parents = {}
    visited = []
    explore = util.Queue()
    actions = []
    current = (problem.getStartState(), None)
    explore.push(current)
    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited:
            current = explore.pop()
        visited.append(current[0])
        neighbors = problem.getSuccessors(current[0])
        for (state, action, cost) in neighbors:
            if state not in visited:
                neighbor = (state, action)
                explore.push(neighbor)
                parents[neighbor] = current
    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()):
            actions.append(current[1])
            current = parents[current]

    return actions[::-1]


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    parents = {}
    visited = []
    explore = util.PriorityQueue()
    actions = []
    current = (problem.getStartState(), None)
    explore.push(current, 0)
    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited:
            current = explore.pop()
        visited.append(current[0])
        neighbors = problem.getSuccessors(current[0])
        for (state, action, cost) in neighbors:
            if state not in visited:
                neighbor = (state, action)
                explore.push(neighbor, cost)
                parents[neighbor] = current
    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()):
            actions.append(current[1])
            current = parents[current]

    return actions[::-1]


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    parents = {}
    visited = []
    explore = util.PriorityQueue()
    actions = []
    current = (problem.getStartState(), None)
    explore.push(current, 0)
    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited:
            current = explore.pop()
        visited.append(current[0])
        neighbors = problem.getSuccessors(current[0])
        for (state, action, cost) in neighbors:
            if state not in visited:
                neighbor = (state, action)
                explore.push(neighbor, heuristic(state, problem))
                parents[neighbor] = current
    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()):
            actions.append(current[1])
            current = parents[current]

    return actions[::-1]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch