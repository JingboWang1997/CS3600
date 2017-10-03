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

    parents = {} #to help tracing back
    visited = []
    explore = util.Stack()
    actions = []
    current = (problem.getStartState(), None) #(position, action)
    explore.push(current)

    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited: #if the popped is visited, skip it
            current = explore.pop()
        if (not problem.isGoalState(current[0])): #to prevent expanding on the goal
            visited.append(current[0])
            neighbors = problem.getSuccessors(current[0])
            for (state, action, cost) in neighbors:
                if state not in visited:
                    neighbor = (state, action)
                    explore.push(neighbor)
                    parents[neighbor] = current

    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()): #trace back
            actions.append(current[1])
            current = parents[current]

    return actions[::-1] #return the actions in the right order

def breadthFirstSearch(problem):

    parents = {} #to help tracing back
    visited = []
    explore = util.Queue()
    actions = []
    current = (problem.getStartState(), None) #(position, action)
    explore.push(current)

    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited: #if the popped is visited, skip it
            current = explore.pop()
        if (not problem.isGoalState(current[0])): #to prevent expanding on the goal
            visited.append(current[0])
            neighbors = problem.getSuccessors(current[0])
            for (state, action, cost) in neighbors:
                if state not in visited:
                    neighbor = (state, action)
                    explore.push(neighbor)
                    parents[neighbor] = current

    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()): #trace back
            actions.append(current[1])
            current = parents[current]

    return actions[::-1] #return the actions in the right order

def uniformCostSearch(problem):

    parents = {} #to help tracing back
    visited = []
    explore = util.PriorityQueue()
    actions = []
    current = (problem.getStartState(), None, 0) #(state, action, cost)

    explore.push(current, 0)
    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited: #if the popped is visited, skip it
            current = explore.pop()
        if not problem.isGoalState(current[0]): #to prevent expanding on the goal
            visited.append(current[0])
            neighbors = problem.getSuccessors(current[0])
            for (state, action, cost) in neighbors:
                if state not in visited:
                    neighbor = (state, action, cost + current[2])
                    explore.push((state, action, cost + current[2]), cost + current[2])
                    parents[neighbor] = current

    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()): #trace back
            actions.append(current[1])
            current = parents[current]

    return actions[::-1] #return the actions in the right order

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
    parents = {} #to help tracing back
    visited = []
    explore = util.PriorityQueue()
    actions = []
    current = (problem.getStartState(), None, heuristic(problem.getStartState(), problem)) #(state, action, heuristic)
    explore.push(current, heuristic(problem.getStartState(), problem))

    while not explore.isEmpty() and not problem.isGoalState(current[0]):
        current = explore.pop()
        while current[0] in visited: #if the popped is visited, skip it
            current = explore.pop()
        if not problem.isGoalState(current[0]): #to prevent expanding on the goal
            visited.append(current[0])
            neighbors = problem.getSuccessors(current[0])
            for (state, action, cost) in neighbors:
                if state not in visited:
                    newH = heuristic(state, problem) + current[2] + cost - heuristic(current[0], problem)
                    #heuristic of new state + stored heuristic in current + cost of path - heuristic of the previous state
                    neighbor = (state, action, newH)
                    explore.push((state, action, newH), newH)
                    parents[neighbor] = current

    if problem.isGoalState(current[0]):
        while (current[0] != problem.getStartState()): #trace back
            actions.append(current[1])
            current = parents[current]

    return actions[::-1] #return the actions in the right order


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch