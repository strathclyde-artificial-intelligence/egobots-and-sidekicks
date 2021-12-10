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
    timeout = int(egobots)*5
    finalplanfile, egosidplanningtime = egobotsidekickv2function.egobotsidekick(filecode, egolist,timeout)
    return

#experimentalsetup = []
egobotsrange = ['04','05','06','07','08','09','10']
goalsrange = ['016'] #if the differences between any of these are smaller than the largest value in locations, bugs will appear
locationsrange = ['04']
sidekicksrange = ['1']
shaperange = ['star']
for egobots in egobotsrange:
    for goals in goalsrange:
        for locations in locationsrange:
            for sidekicks in sidekicksrange:
                for shape in shaperange:
                    runtest(egobots,goals,locations,sidekicks,shape)

