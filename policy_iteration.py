#!/usr/bin/env py

import copy
import random
import numpy as np

eastMatrix = [[0.0 for x in xrange(81 + 1)] for y in xrange(81 + 1)]   # matrix[s][s'] = P(s' | s, a = east) ***0 index is never valid***
southMatrix = [[0.0 for x in xrange(81 + 1)] for y in xrange(81 + 1)]   # matrix[s][s'] = P(s' | s, a = south) ***0 index is never valid***
westMatrix = [[0.0 for x in xrange(81 + 1)] for y in xrange(81 + 1)]   # matrix[s][s'] = P(s' | s, a = west) ***0 index is never valid***
northMatrix = [[0.0 for x in xrange(81 + 1)] for y in xrange(81 + 1)]   # matrix[s][s'] = P(s' | s, a = north) ***0 index is never valid***

actions = [eastMatrix, southMatrix, westMatrix, northMatrix]
rewards = [0.0 for x in xrange(81 + 1)]   # rewards[s] = reward at state s ***0 index is never valid***

def initVar(eastMatrix, southMatrix, westMatrix, northMatrix, rewards):
    # East
    for line in open("/Users/Hanschristian/Desktop/cse150/HW05/assignment5_data/prob_east.txt"):
        line = line.split()
        eastMatrix[int(line[0])][int(line[1])] = float(line[2])
    # South
    for line in open("/Users/Hanschristian/Desktop/cse150/HW05/assignment5_data/prob_south.txt"):
        line = line.split()
        southMatrix[int(line[0])][int(line[1])] = float(line[2])
    # West
    for line in open("/Users/Hanschristian/Desktop/cse150/HW05/assignment5_data/prob_west.txt"):
        line = line.split()
        westMatrix[int(line[0])][int(line[1])] = float(line[2])
    # North
    for line in open("/Users/Hanschristian/Desktop/cse150/HW05/assignment5_data/prob_north.txt"):
        line = line.split()
        northMatrix[int(line[0])][int(line[1])] = float(line[2])
    # Reward
    i = 1
    for line in open("/Users/Hanschristian/Desktop/cse150/HW05/assignment5_data/rewards.txt"):
        rewards[i] = float(line)
        i = i + 1
    return

def policyIteration(actions, rewards, discount):
    '''
    def policyEvaluation(pi, rewards, discount):
        util = [0.0 for x in xrange(81 + 1)]   # Utilities for states in S ***0 index is never valid***
        for s in xrange(1, 81 + 1):
            # Calculate summation
            summation = 0.0
            for sNext in xrange(1, 81 + 1):
                summation = summation + ((pi[s])[s][sNext] * util[sNext])
            # Update util
            util[s] = rewards[s] + (discount * summation)
        return util 
    '''
    def policyEvaluation(pi, rewards, discount):
        matrix = [[0.0 for x in xrange(81)] for y in xrange(81)]   # [0, 80]
        constMatrix = [0.0 for x in xrange(81)]   # [0, 80]
        for s in xrange(1, 81 + 1):
            # Initialize matrix and constMatrix
            for sNext in xrange(1, 81 + 1):
                if sNext == s:
                    matrix[s - 1][sNext - 1] = 1 - (discount * (pi[s])[s][sNext])
                else:
                    matrix[s - 1][sNext - 1] = 0 - (discount * (pi[s])[s][sNext])
            constMatrix[s - 1] = rewards[s]
        # Calculate the matrix
        a = np.array(matrix)
        b = np.array(constMatrix)
        x = np.linalg.solve(a, b)
        # Convert format
        util = [0.0 for z in xrange(81 + 1)]   # Utilities for states in S ***0 index is never valid***
        for i in xrange(1, 81 + 1):
            util[i] = x[i - 1]
        return util
    
    pi = [None for x in xrange(81 + 1)]   # Policy for states in S ***0 index is never valid***
    # Initialize pi to random
    for i in xrange(1, 81 + 1):
        pi[i] = actions[random.randint(0, 3)]
    
    while (True):
        util = policyEvaluation(pi, rewards, discount)
        unchanged = True
        for s in xrange(1, 81 + 1):
            # Calculate max term
            maxList = []
            maxActionList = []
            for a in actions:
                summation = 0.0
                for sNext in xrange(1, 81 + 1):
                    summation = summation + (a[s][sNext] * util[sNext])
                maxList = maxList + [summation]
                maxActionList = maxActionList + [a]
            maxIndex = maxList.index(max(maxList))
            maxResult = maxList[maxIndex]   # Save for branch
            maxAction = maxActionList[maxIndex]   # Save for branch
            # Calculate term without max
            summation = 0.0   # Save for branch
            for sNext in xrange(1, 81 + 1):
                summation = summation + ((pi[s])[s][sNext] * util[sNext])
            # Branch
            if maxResult > summation:
                pi[s] = maxAction
                unchanged = False
        if unchanged:
            break
    return pi

# main
initVar(eastMatrix, southMatrix, westMatrix, northMatrix, rewards)
# 2c
print "----------2c----------\n"
pi = policyIteration(actions, rewards, 0.99)
for i in xrange(1, 81 + 1):
    a = ""
    if pi[i] == eastMatrix:
        a = "EAST"
    elif pi[i] == southMatrix:
        a = "SOUTH"
    elif pi[i] == westMatrix:
        a = "WEST"
    elif pi[i] == northMatrix:
        a = "NORTH"
    print "(" + str(i) + ", " + a + ")"
