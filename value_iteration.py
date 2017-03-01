#!/usr/bin/env py

import copy

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

def valueIteration(actions, rewards, discount, maxError):
    util = [0.0 for x in xrange(81 + 1)]   # Utilities for states in S ***0 index is never valid***
    utilNext = [0.0 for x in xrange(81 + 1)]
    pi = [None for x in xrange(81 + 1)]   # Optimal policy for states in S ***0 index is never valid***
    while (True):
        util = copy.deepcopy(utilNext)
        maxUtilChange = 0
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
            # Update utilNext
            maxIndex = maxList.index(max(maxList))
            utilNext[s] = rewards[s] + (discount * maxList[maxIndex])
            pi[s] = maxActionList[maxIndex]
            # Check Util change
            if (utilNext[s] - util[s]) > maxUtilChange:
                maxUtilChange = utilNext[s] - util[s]
        if maxUtilChange < (((1 - discount) * maxError) / discount):
            break
    return util, pi

# main
initVar(eastMatrix, southMatrix, westMatrix, northMatrix, rewards)
util, pi = valueIteration(actions, rewards, 0.99, 0.01)
# 2a
print "----------2a----------\n"
for i in xrange(1, 81 + 1):
    if util[i] != 0:
        print "v(" + str(i) + ") = " + str(util[i])
# 2b
print "\n----------2b----------\n"
for i in xrange(1, 81 + 1):
    if util[i] != 0:
        a = ""
        if pi[i] == eastMatrix:
            a = "EAST"
        elif pi[i] == southMatrix:
            a = "SOUTH"
        elif pi[i] == westMatrix:
            a = "WEST"
        elif pi[i] == northMatrix:
            a = "NORTH"
        print "(" + str(i) + ", " + str(util[i]) + ", " + a + ")"
