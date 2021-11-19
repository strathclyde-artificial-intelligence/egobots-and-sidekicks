# egosidtester.py
# This file calls on the egobot sidekick framework and on the egobot sidekick problem generator to run tests.

import os
import egobotsidekickv2function
import egosidproblemgenerator

def runtest(egobots,goals,locations,sidekicks,shape):
    #egobots = settings[0]
    #goals = settings[1]
    #locations = settings[2]
    #sidekicks = settings[3]
    #shape = settings[4]

    filecode, egolist = egosidproblemgenerator.generate(egobots,goals,locations,sidekicks,shape)
    egobotsidekickv2function.egobotsidekick(filecode, egolist)
    return

#experimentalsetup = []
egobotsrange = ['02','01']
goalsrange = ['004','008','016'] #if the differences between any of these are smaller than the largest value in locations, bugs will appear
locationsrange = ['04']
sidekicksrange = ['1']
shaperange = ['ring']
for egobots in egobotsrange:
    for goals in goalsrange:
        for locations in locationsrange:
            for sidekicks in sidekicksrange:
                for shape in shaperange:
                    runtest(egobots,goals,locations,sidekicks,shape)

