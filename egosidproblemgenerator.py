# egosidproblemgenerator.py
# This file defines a function which can be called on to generate problem files and a filecode for those files.

import math
import random

def generate(egobots, goals, locations, sidekicks, shape):
    if shape != 'star':
        shape = 'ring'

    numegobots = int(egobots)
    numgoals = int(goals)
    numlocations = int(locations)
    numsidekicks = int(sidekicks)

    goalsperloc = math.ceil(numgoals/numlocations)

    goals = str(goalsperloc*numlocations)
    numgoals = int(goals)
    if len(goals) == 1:
        goals = '0'+goals
    if len(goals) == 2:
        goals = '0'+goals
    filecode = egobots+goals+locations+sidekicks+shape
    numcomplexgoals = math.floor(numgoals/5)

    objects = {
        'locations': '',
        'sidekicks': '',
        #'egobots': '',
        'panels': '',
        'welders': '',
        'patches': ''
    }

    init = {
        'egobot-adjacent': '',
        'sidekick-adjacent': '',
        'pick-up-valid': '',
        'panel-at': '',
        'sid': '',
        'ego': [],
        'not-handled': [],
        'dropped': ';welderstart\n'
    }

    goals = []
    patchcount = 0
    
    locationlist = []
    for i in range(1,numegobots+1):
        stri = str(i)
        if len(stri) == 1:
            stri = '0'+stri
        goals.append('')
        temploclist = []
        goalcountdown = numgoals
        complexgoalcountdown = numcomplexgoals
        for j in range(1,numlocations+1):
            strj = str(j)
            if len(strj) == 1:
                strj = '0'+strj
            templocation = 'l'+stri+strj
            for k in range(1,goalsperloc+1):
                strk = str(k)
                if len(strk) == 1:
                    strk = '0'+strk
                objects['panels'] = objects['panels'] + 'pn'+stri+strj+strk+' '
                init['panel-at'] = init['panel-at'] + '(panel-at pn'+stri+strj+strk+' '+templocation+')\n'
                if random.randint(1,goalcountdown+1) <= complexgoalcountdown:
                    if random.randint(0,2):
                        goals[i-1] = goals[i-1] + '(is-welded pn'+stri+strj+strk+')\n'
                    else:
                        goals[i-1] = goals[i-1] + '(is-patched pn'+stri+strj+strk+')\n'
                        patchcount = patchcount+1
                    complexgoalcountdown = complexgoalcountdown-1
                else:
                    goals[i-1] = goals[i-1] + '(is-inspected pn'+stri+strj+strk+')\n'
                goalcountdown = goalcountdown-1
            locationlist.append(templocation)
            objects['locations'] = objects['locations']+templocation+' '
            temploclist.append(templocation)
        for j in range(0, len(temploclist)-1):
            init['egobot-adjacent'] = init['egobot-adjacent']+'(egobot-adjacent '+temploclist[j] + ' ' + temploclist[j+1] + ')'+'\n' + '(egobot-adjacent '+temploclist[j+1] + ' ' + temploclist[j] + ')'+'\n'
        if shape == 'star':
            for j in range(0, len(temploclist)-1):
                init['sidekick-adjacent'] = init['sidekick-adjacent']+'(sidekick-adjacent '+temploclist[j] + ' ' + temploclist[j+1] + ')'+'\n' + '(sidekick-adjacent '+temploclist[j+1] + ' ' + temploclist[j] + ')'+'\n'

    if shape == 'ring':
        lenloclist = len(locationlist)
        for i in range(0,lenloclist-1):
            init['sidekick-adjacent'] = init['sidekick-adjacent']+'(sidekick-adjacent '+locationlist[i] + ' ' + locationlist[i+1] + ')'+'\n' + '(sidekick-adjacent '+locationlist[i+1] + ' ' + locationlist[i] + ')'+'\n'
        init['sidekick-adjacent'] = init['sidekick-adjacent']+'(sidekick-adjacent '+locationlist[-1] + ' ' + locationlist[0] + ')'+'\n' + '(sidekick-adjacent '+locationlist[0] + ' ' + locationlist[-1] + ')'+'\n'
        init['sidekick-adjacent'] = init['sidekick-adjacent']+'(sidekick-adjacent '+locationlist[-1] + ' ' + 'lsid' + ')'+'\n' + '(sidekick-adjacent '+'lsid' + ' ' + locationlist[-1] + ')'+'\n'
        init['sidekick-adjacent'] = init['sidekick-adjacent']+'(sidekick-adjacent '+'lsid' + ' ' + locationlist[0] + ')'+'\n' + '(sidekick-adjacent '+locationlist[0] + ' ' + 'lsid' + ')'+'\n'
        locationlist.append('lsid')
        objects['locations'] = objects['locations']+'lsid'+' '
    
    if shape == 'star':
        for i in range(numegobots):
            init['sidekick-adjacent'] = init['sidekick-adjacent']+'(sidekick-adjacent '+locationlist[i*numlocations] + ' ' + 'lsid' + ')'+'\n' + '(sidekick-adjacent '+'lsid' + ' ' + locationlist[i*numlocations] + ')'+'\n'
        locationlist.append('lsid')
        objects['locations'] = objects['locations']+'lsid'+' '
    
    for loc in locationlist:
        init['pick-up-valid'] = init['pick-up-valid'] + '(welder-pick-up-valid '+loc+')\n' + '(patch-pick-up-valid '+loc+')\n'

    for i in range(1,numsidekicks+1):
        objects['sidekicks'] = objects['sidekicks'] + 'sid'+str(i)+' '
        tempsidstr = ';sidlocstart\n(at sid'+str(i)+' lsid)\n;sidlocend\n(camera-free sid'+str(i)+')\n(hands-free sid'+str(i)+')\n'
        init['sid'] = init['sid'] + tempsidstr

    egolist = []
    for i in range(1, numegobots+1):
        stri = str(i)
        if len(stri) == 1:
            stri = '0'+stri
        egolist.append(stri)
        tempegostr = '(at ego'+stri+' '+locationlist[(i-1)*numlocations+1]+')\n(camera-free ego'+stri+')\n(hands-free ego'+stri+')\n'
        init['ego'].append(tempegostr)
        temphandledstr = ''
        for j in range(1,patchcount+1):
            strj = str(j)
            if len(strj) == 1:
                strj = '0'+strj
            temphandledstr = temphandledstr + '(not-handled ego'+stri+' pa'+strj+')\n'
            for k in range(1,numsidekicks+1):
                temphandledstr = temphandledstr + '(not-handled sid'+str(k)+' pa'+strj+')\n'
        for j in range(1,numegobots):
            strj = str(j)
            if len(strj) == 1:
                strj = '0'+strj
            temphandledstr = temphandledstr + '(not-handled ego'+stri+' w'+strj+')\n'
            for k in range(1,numsidekicks+1):
                temphandledstr = temphandledstr + '(not-handled sid'+str(k)+' w'+strj+')\n'
        init['not-handled'].append(temphandledstr)

    for i in range(numegobots-1):
        stri = str(i+1)
        if len(stri) == 1:
            stri = '0'+stri
        objects['welders'] = objects['welders'] + 'w'+stri+' '
        init['dropped'] = init['dropped'] + '(dropped w'+stri+' lsid)\n'
    
    init['dropped'] = init['dropped']+';welderend\n;patchstart\n'

    for i in range(patchcount):
        stri = str(i+1)
        if len(stri) == 1:
            stri = '0'+stri
        objects['patches'] = objects['patches'] + 'pa'+stri+' '
        init['dropped'] = init['dropped'] + '(dropped pa'+stri+' lsid)\n'
    
    init['dropped'] = init['dropped']+';patchend\n'
    
    for i, goalstr in enumerate(goals):
        goals[i] = goalstr + '(hands-free ego'+egolist[i]+')\n\n'

    egopt1 = filecode+'egobot-'
    egopt2 = '-problem-1.pddl'
    sidfileempty = filecode+'sidekick-problem-empty-3.pddl'
    fullproblem = filecode+'full-problem.pddl'

    egofiles = []
    fullego = ''
    for i in egolist:
        egofiles.append(egopt1+i+egopt2)
        fullego = fullego + 'ego'+i+' '
    
    define = '(define (problem problem_name) (:domain maintenance-domain-gobjects)\n'

    sidobjectstr = '(:objects \n'+objects['locations']+'- location\n'+objects['sidekicks']+'- sidekick\n'+objects['panels']+'- panel\n'+objects['welders']+'- welder\n'+objects['patches']+'- patch\n)\n\n'
    sidinitstr = '(:init \n'+init['egobot-adjacent']+init['sidekick-adjacent']+init['sid']+init['dropped']+init['panel-at']+init['pick-up-valid']+'\n;inspectrequests\n\n;welderrequests\n\n;patchrequests\n\n(deadline-open)\n\n(= (score) 0)\n)\n'
    sidgoalstr = '(:goal (and\n;goalstart\n(> (score) 0)\n;goalend\n))\n'
    sidendstr = '\n(:metric maximize (score))\n\n)'

    f = open(sidfileempty,'x')
    f.write(define+sidobjectstr+sidinitstr+sidgoalstr+sidendstr)
    f.close()

    fullobjectstr = '(:objects \n'+objects['locations']+'- location\n'+objects['sidekicks']+'- sidekick\n'+fullego+'- egobot\n'+objects['panels']+'- panel\n'+objects['welders']+'- welder\n'+objects['patches']+'- patch\n)\n\n'
    fullinitstr = '(:init \n'+init['egobot-adjacent']+init['sidekick-adjacent']+init['sid']
    for i in range(numegobots):
        fullinitstr = fullinitstr + init['ego'][i]
    fullinitstr = fullinitstr+init['dropped']+init['panel-at']+'\n\n(deadline-open)\n)\n'
    fullgoalstr = '(:goal (and\n'
    for i in range(numegobots):
        fullgoalstr = fullgoalstr + goals[i]
    fullgoalstr = fullgoalstr+'))\n\n'
    fullendstr = ')'

    f = open(fullproblem,'x')
    f.write(define+fullobjectstr+fullinitstr+fullgoalstr+fullendstr)
    f.close

    for i, goal in enumerate(goals):
        stri = str(i+1)
        if len(stri) == 1:
            stri = '0'+stri
        egoobjectstr = '(:objects \n'+objects['locations']+'- location\n'+objects['sidekicks']+'- sidekick\nego'+stri+' - egobot\n'+objects['panels']+'- panel\n'+objects['welders']+'- welder\n'+objects['patches']+'- patch\n)\n\n'
        egoinitstr = '(:init \n'+init['egobot-adjacent']+init['sidekick-adjacent']+init['sid']+init['ego'][i]+init['not-handled'][i]+init['dropped']+init['panel-at']+'\n(deadline-open)\n)\n\n'
        egogoalstr = '(:goal (and\n;goalstart\n'+goal+';goalend\n))\n\n'
        egoendstr = ')'
        f = open(egofiles[i],'x')
        f.write(define+egoobjectstr+egoinitstr+egogoalstr+egoendstr)
        f.close()

    return filecode, egolist

#generate('04','016','04','1','ring')