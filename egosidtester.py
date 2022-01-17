# egosidtester.py
# This file calls on the egobot sidekick framework and on the egobot sidekick problem generator to run tests.

import os
import egobotsidekickv2function
import egosidproblemgenerator
import sys

if len(sys.argv)<3:
    print ("USAGE: python3"+str(sys.argv[0])+" no_egobots no_goals")
    sys.exit(0)

def runtest(egobots,goals,locations,sidekicks,shape):
    #egobots = settings[0]
    #goals = settings[1]
    #locations = settings[2]
    #sidekicks = settings[3]
    #shape = settings[4]

    filecode, egolist = egosidproblemgenerator.generate(egobots,goals,locations,sidekicks,shape)
    timeout = int(egobots)*5*int(locations)
    finalplanfile, egosidplanningtime = egobotsidekickv2function.egobotsidekick(filecode, egolist,timeout)
    return

#experimentalsetup = []
egobotsrange = str(sys.argv[1])
if len(sys.argv[1]) < 2: egobotsrange = "0"+egobotsrange

locationsrange = str(sys.argv[2])
if len(sys.argv[2]) < 2: locationsrange = "0"+locationsrange

key = ''
if len(sys.argv) > 3:
    key = str(sys.argv[3])

#goalsrange = ['016'] #if the differences between any of these are smaller than the largest value in locations, bugs will appear
#locationsrange = ['04']
sidekicksrange = ['1']
shaperange = ['star']
for egobots in [egobotsrange]:
    #for goals in goalsrange:
    for locations in [locationsrange]:
        goals = str(int(locations)*4)
        if len(goals) == 2:
            goals = '0'+goals
        for sidekicks in sidekicksrange:
            for shape in shaperange:
                runtest(egobots,goals,locations,sidekicks,shape,key)

