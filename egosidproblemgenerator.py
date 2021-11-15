# egosidproblemgenerator.py
# This file defines a function which can be called on to generate problem files and a filecode for those files.

import os

def generate(egobots, goals, locations, sidekicks, shape):
    filecode = egobots+goals+locations+sidekicks+shape

    numegobots = int(egobots)
    numgoals = int(goals)
    numlocations = int(locations)
    numsidekicks = int(sidekicks)

    egolist = []
    for i in range(1, numegobots+1):
        egolist.append(str(i))

    

    return filecode, egolist