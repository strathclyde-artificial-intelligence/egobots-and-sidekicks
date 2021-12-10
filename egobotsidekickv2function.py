# egobotsidekickv2.py
# This file is a work in progress.
# This file aims to achieve the full functionality of egobotsidekick.py, but with a better framework that allows new parsing rules to be added more easily.
# This file uses the Agent class and the Action subclass to define rules for how to parse a plan.
# This file uses general functions for parsing plans. These parsing functions must be tweaked to suit the output format of a planner.
# This file uses separate functions for each modification to or addition of a line to a problem file.

import os

class Agent:
    def __init__(self, name = 'undefined', *listactions):
        self.name = name
        self.actions = []
        for x in listactions:
            obj = self.Action(x)
            self.actions.append(obj)
    
    def get_data(self):
        print('This Agent has ' + str(len(self.actions)) + ' parsing-relevant actions, listed below.')
        for i, x in enumerate(self.actions):
            print(self.actions[i].get_data())

    class Action:
        def __init__(self, name = 'undefined'):
            self.name = name #a name
            self.identifiers = 'undefined' #the strings which identify this action is in a plan
            self.parsing = [['undefined','undefined']] #a list of pairs of strings which can be used to isolate any pieces of information which must be recorded
            self.function = 'undefined' #the names of any functions used to add or modify the next problem file based on reading this action in the previous plan
        
        def set_identifiers(self, *identifiers):
            self.identifiers = identifiers
        
        def set_parsing(self, parsing = [['undefined','undefined']]):
            self.parsing = parsing

        def set_function(self, functionname):
            self.function = functionname

        def get_data(self):
            print('Action: ' + self.name)
            print('Identifier: ' + str(self.identifiers))
            print('Parsing Borders: ' + str(self.parsing))
            print('Function Names: ' + str(self.function))

# These are the file modification functions

def addinspectrequest(file, parsedinfo, deadline):
    panels = parsedinfo[0]
    sep1 = file.partition(';inspectrequests') # this comment must be added in the :init section of the empty sidekick problem
    newfile = sep1[0]+sep1[1]
    for panel in panels:
        newfile = newfile + '\n'+'(= (ingoal '+panel+') 1)'+'\n'+'(is-not-inspected '+panel+')'+'\n'+'(at '+deadline+' (not (is-not-inspected '+panel+')))'
    newfile = newfile+sep1[2]
    score = 1
    return newfile, score

def addwelderrequest(file, parsedinfo, deadline):
    droplocations = parsedinfo[0]
    sep1 = file.partition(';welderrequests') # this comment must be added in the :init section of the empty sidekick problem
    newfile = sep1[0]+sep1[1]
    if not '(welder-needed)' in sep1[2]:
        newfile = newfile + '\n(welder-needed)'
    for i, droplocation in enumerate(droplocations):
        newfile = newfile + '\n'+'(= (wegoal '+droplocation+' 10)'+'\n'+'(welder-drop-needed '+droplocation+'\n'+'(at '+str(float(deadline)+3.003)+' (not (welder-drop-needed '+droplocation+'))' #hopefully 3.003 makes up for a problem with incorrect welder locations
    newfile = newfile+sep1[2]
    score = 10
    return newfile, score

def addpatchrequest(file, parsedinfo, deadline):
    droplocations = parsedinfo[0]
    patches = parsedinfo[1]
    patchsep1 = file.partition(';patchstart')
    patchsep2 = patchsep1[2].partition(';patchend')
    patchsep3 = patchsep2[0].splitlines()
    newpatches = ''
    for line in patchsep3:
        if any(patch in line for patch in patches):
            newpatches = newpatches + '\n' + line + ';patchbodge'
        else:
            newpatches = newpatches + '\n' + line
    newfile = patchsep1[0]+patchsep1[1]+newpatches+'\n'+patchsep2[1]+patchsep2[2]
    sep1 = newfile.partition(';patchrequests')
    newfile = sep1[0]+sep1[1]
    if not '(patch-needed)' in sep1[2]:
        newfile = newfile + '\n(patch-needed)'
    for i, droplocation in enumerate(droplocations):
        newfile = newfile + '\n'+'(= (pagoal '+droplocation+' 10)'+'\n'+'(patch-drop-needed '+droplocation+'\n'+'(at '+deadline+' (not (patch-drop-needed '+droplocation+'))'
    newfile = newfile+sep1[2]
    score = 10
    return newfile, score

def addegowelderdrop(file, welders, locations, times):
    sep1 = file.partition(';welderstart')
    newfile = sep1[0]+sep1[1]+'\n'
    sep2 = sep1[2].partition(';welderend')
    sep3 = sep2[0].splitlines()
    for line in sep3:
        linecheck = 0
        for i, welder in enumerate(welders):
            if welder in line:
                newfile = newfile + '(at ' + times[i] + ' (dropped ' + welder + ' ' + locations[i] + '))\n'
                linecheck = 1
        if linecheck == 0:
            newfile = newfile + line + '\n'
    newfile = newfile + sep2[1] + sep2[2]
    return newfile

def removepatch(file, parsedinfo, placeholder):
    #patches = parsedinfo[0]
    sep1 = file.partition(';patchstart')
    sep2 = sep1[2].partition(';patchend')
    #sep3 = sep2[0].splitlines()
    #newpatches = ''
    #for line in sep3:
    #    if any(patch in line for patch in patches) and not ';patchbodge' in line:
    #        newpatches = newpatches + '\n;' + line
    #    else:
    #        newpatches = newpatches + '\n' + line
    newfile = sep1[0]+sep1[1]+patchset+'\n'+sep2[1]+sep2[2]
    score = 0
    return newfile, score


def modifyinspectgoal(file, parsedinfo, placeholder): # this function takes in a list of all the panels, if you do only one panel at a time it will be slower
    panels = parsedinfo[0]
    sep1 = file.partition(';goalstart') # this comment must be located at the start of the egobot's goals
    sep2 = sep1[2].partition(';goalend') # this comment must be located at the end of the egobot's goals
    sep3 = sep2[0].splitlines()
    newgoals = ''
    for line in sep3:
        if any(panel in line for panel in panels):
            if 'is-inspected' in line:
                newgoals = newgoals + '\n'+';'+line
            else:
                newgoals = newgoals + '\n'+line
        else:
            newgoals = newgoals + '\n'+line
    newfile = sep1[0]+sep1[1]+newgoals+'\n'+sep2[1]+sep2[2]
    return newfile

def addwelderdrop(file, parsedinfo, droptimes):
    locations = parsedinfo[0]
    welders = parsedinfo[1]
    sep1 = file.partition(';welderstart') #these comments must be placed before and after the list of welder locations in the egobot problem files
    newwelders = '\n'
    for i, welder in enumerate(welders):
        newwelders = newwelders +'(at '+droptimes[i]+' (dropped '+welder+' '+locations[i]+')' + '\n'
    #sep2 = sep1[2].partition(';welderend')
    #sep3 = sep2[0].splitlines()
    #for i, welder in enumerate(welders):
    #    for j, line in enumerate(sep3):
    #        if welder in line:
    #            sep3[j] = '(at '+droptimes[i]+' (dropped '+welder+' '+locations[i]+')' #This doesn't allow a welder to be dropped, used, picked up, dropped elsewhere, and used again
    #newwelders = ''
    #for line in sep3:
    #    newwelders = newwelders + line + '\n'
    newfile = sep1[0]+sep1[1]+newwelders+sep1[2]
    return newfile

def addpatchdrop(file, parsedinfo, droptimes):
    locations = parsedinfo[0]
    patches = parsedinfo[1]
    sep1 = file.partition(';patchstart') # these comments must be found in the egobot problem files
    sep2 = sep1[2].partition(';patchend')
    sep3 = sep2[0].splitlines()
    egobotsep1 = sep1[0].partition(' - egobot')
    egobotsep2 = egobotsep1[0].partition('ego')
    egobotnum = egobotsep2[2]
    global patchset
    for i, patch in enumerate(patches):
        for j, line in enumerate(sep3):
            if patch in line:
                if locations[i][1]+locations[i][2] in egobotnum: # this would delete patches dropped in previous iterations if not for the for i, patch in enumerate(patches) line
                    sep3[j] = '(at '+droptimes[i]+' (dropped '+patch+' '+locations[i]+')'
                    patchsetlines = patchset.splitlines()
                    for k, setline in enumerate(patchsetlines):
                        if patch in setline:
                            patchsetlines[k] = ';'
                    patchset = '\n'.join(patchsetlines)
                else:
                    sep3[j] = ''
    newpatches = ''
    for line in sep3:
        newpatches = newpatches + line + '\n'
    newfile = sep1[0]+sep1[1]+newpatches+sep2[1]+sep2[2]
    #this next bit of the function corrects the sidekick's knowledge of the world in cases of the egobot requesting too many patches
    patchavailablecount = 0
    for line in sep3:
        if '(at ' in line:
            patchavailablecount = patchavailablecount + 1
    goalsep1 = file.partition(';goalstart')
    goalsep2 = goalsep1[2].partition(';goalend')
    patchrequiredcount = goalsep2[0].count('is-patched')
    patchfixer = 0
    while patchavailablecount > patchrequiredcount:
        patchset = patchset + '\n(dropped '+patches[patchfixer]+' '+locations[patchfixer] # the last ')' is contained in the locations string for not a very good reason
        patchfixer = patchfixer + 1 #if this exceeded the index of patches, something has gone terribly wrong
        patchavailablecount = patchavailablecount - 1
    return newfile

def modifysidekicklocation(file, sidloc, sidtime):
    sep1 = file.partition(';sidlocstart') # this comment must be placed before the sidekick's starting location in the egobot problem file
    sep2 = sep1[2].partition(';sidlocend') # this comment must be placed after
    newfile = sep1[0]+sep1[1]+ '\n'+'(at '+sidtime+' (at sid1 '+sidloc+'))\n'+sep2[1]+sep2[2]
    return newfile

def modifysidekickstart(file, sidloc):
    sep1 = file.partition(';sidlocstart') # this comment must be placed before the sidekick's starting location in the empty sidekick problem file
    sep2 = sep1[2].partition(';sidlocend') # this comment must be placed after
    newfile = sep1[0]+sep1[1]+ '\n'+' (at sid1 '+sidloc+')\n'+sep2[1]+sep2[2]
    return newfile

def modifysidekickgoal(file, minscore): # minscore must be a string
    sep1 = file.partition(';goalstart')
    sep2 = sep1[2].partition(';goalend')
    newfile = sep1[0]+sep1[1]+'\n'+'(> (score) '+minscore+')'+'\n'+sep2[1]+sep2[2]
    return newfile

# These are the parser functions

def outputparser(file): # this function extracts a plan from a planner's output log
    splitbyplan = file.split('; Time ')
    lastplan = '0.000:' + splitbyplan[-1]
    lastplanlines = lastplan.splitlines()
    plan = ''
    for line in lastplanlines:
        if ': (' in line:
            plan = plan + '\n' + line
    timesep1 = splitbyplan[-1].partition('\n')
    planningtime = float(timesep1[0])
    return plan, planningtime

def planparser(plan, action): # this function parses a plan string for information contained in the parsing pairs on lines identified by identifiers
    planlines = plan.splitlines()
    identifiers = action.identifiers
    print(str(identifiers))
    parsing = action.parsing
    relevantlines = []
    keyinfo = []
    deadlines =[]
    for i, pair in enumerate(parsing):
        keyinfo.append([])
    for line in planlines:
        if all(key in line for key in identifiers): # the line must contain every identifier string to be accepted
            relevantlines.append(line)
            print(line)
    for line in relevantlines:
        for i, pair in enumerate(parsing): # parsing is a list of lists of strings, each list of strings has two strings
            sep1 = line.partition(pair[0]) # cut off the part of the line before the info to be parsed
            sep2 = sep1[2].partition(pair[1]) # cut off the part of the line after the info to be parsed
            keydatum = sep1[1]+sep2[0]+sep2[1] # combine the parsing strings with the contained string
            keyinfo[i].append(keydatum.strip()) # the spaces used in the parsing strings are removed by the .strip()
        timesep1 = line.partition(':')
        deadlines.append(str(float(timesep1[0])+0.005))
    #if relevantlines:
    #    lastrelevantline = relevantlines[-1]
    #    timesep1 = lastrelevantline.partition(':') # extract starting time of the last line
    #    #timesep2a = timesep1[2].partition(' [') # extract duration of the last line
    #    #timesep2b = timesep2a[2].partition(']') # trim square bracket off the duration
    #    lastlinestart = timesep1[0]
    #    #lastlinedur = timesep2b[0]
    #    deadline = str(float(lastlinestart)+0.005)#+float(lastlinedur))
    #    # 0.005 second buffer has been added due to an error which occured when the sidekick had only one request to deal with and that request was at its starting location, thus having a deadline of 0.001 seconds
    #else:
    #    deadline = 0
    return keyinfo, deadlines # a list of lists of strings such as panels and a list of strings giving the start time of each action

def endlocationparser(plan):
    planlines = plan.splitlines()
    lastline = planlines[-1]
    timesep1 = lastline.partition(':') # extract the starting time of the last line
    timesep2a = timesep1[2].partition(' [') # extract duration of last line
    timesep2b = timesep2a[2].partition(']') # trim square bracket off the duration
    lastlinestart = timesep1[0]
    lastlinedur = timesep2b[0]
    endtime = str(float(lastlinestart)+float(lastlinedur))
    locsep1 = lastline.partition(' l') # cut off the part of the last line before the location in that final action (this might be inaccurate for a move action)
    locsep2 = locsep1[2].partition(')') # cut off the part of the last line after the location
    endloc = locsep1[1]+locsep2[0]
    endloc = endloc.strip()
    return endtime, endloc

def egowelderdropparser(plan):
    planlines = plan.splitlines()
    welders = []
    locations = []
    times = []
    requestchecker = 0
    for line in planlines:
        if 'sid' and 'drop-welder' in line:
            requestchecker = 1
        if 'ego' and 'drop-welder' in line and requestchecker == 0:
            timesep1 = line.partition(':')
            timesep2 = timesep1[2].partition(' [')
            timesep3 = timesep2[2].partition(']')
            droptime = str(float(timesep1[0])+float(timesep3[0]))
            times.append(droptime)
            weldsep1 = line.partition(' w')
            weldsep2 = weldsep1[2].partition(' ')
            welders.append('w'+weldsep2[0])
            locsep1 = line.partition(' l')
            locsep2 = locsep1[2].partition(')')
            locations.append('l'+locsep2[0])
    return welders, locations, times

# This function calls a planner

def callplanner(planner,domain,problem,planfile,timeout): # all as strings, give full file names for domain, problem, and planfile. include modifiers like -n in planner
    f = open(planfile,'x')
    f.close()
    arg = 'timeout '+timeout+' '+'./'+planner+' '+domain+' '+problem+' > '+planfile
    os.system(arg)
    f = open(planfile,'r')
    outputlog = f.read()
    f.close()
    return outputlog

# Here strings are defined which are used to find and create files.
def egobotsidekick(filecode, egolist, timeoutint):
    egopt1 = filecode+'egobot-'
    egopt2 = '-problem-'
    egopt3 = filecode+'Egobot-'
    egopt4 = '-Iteration-'

    sidpt1 = filecode+'sidekick-problem-'
    sidpt2 = filecode+'Sidekick-Iteration-'

    fullproblemfile = filecode+'full-problem.pddl'

    fullplanfile = filecode+'Single-Agent-Plan.txt'

    finalplanfile = filecode+'Final-Plan.txt'

    # Here the empty sidekick problem is named.
    sidfileempty = filecode+'sidekick-problem-empty-3.pddl'
    f = open(sidfileempty,'r')
    sidempty = f.read()
    f.close()

    # Here the domains are named.
    egodomain = 'egobot-domain.pddl'
    siddomain = 'sidekick-domain-3.pddl'
    fulldomain = 'maintenance-domain-2.pddl'

    # Here the planner is named.
    planner = 'optic-cplex -n'

    # Here the iteration counting variable and the success variable are made.
    iter = 1
    iterstr = str(iter)
    success = 0
    egosuccess = []
    for x in egolist:
        egosuccess.append(0)
    print(str(egosuccess))

    timeoffset = 0.0

    planningtimetotal = 0.0

    # Here the egobot input file names are found.
    egobotproblemfiles = []
    egobotplanfiles = []
    for egobotnum in egolist:
        egobotproblemfiles.append(egopt1+egobotnum+egopt2+iterstr+'.pddl')
        egobotplanfiles.append(egopt3+egobotnum+egopt4+iterstr+'.txt')

    # Here the agents and actions are created.
    egotosid = Agent('sid','inspect','dropwelder','droppatch','removepatch')#,'egodropwelder')

    egotosid.actions[0].set_identifiers('sid','inspect')
    egotosid.actions[0].set_parsing([[' pn',' ']])
    egotosid.actions[0].set_function('addinspectrequest')

    egotosid.actions[1].set_identifiers('sid','drop-welder')
    egotosid.actions[1].set_parsing([[' l',' ']])
    egotosid.actions[1].set_function('addwelderrequest')

    egotosid.actions[2].set_identifiers('sid','drop-patch')
    egotosid.actions[2].set_parsing([[' l',' '],[' pa',' ']])
    egotosid.actions[2].set_function('addpatchrequest')

    egotosid.actions[3].set_identifiers('ego','apply-patch')
    egotosid.actions[3].set_parsing([[' pa',' ']])
    egotosid.actions[3].set_function('removepatch')

    #egotosid.actions[3].set_identifiers('ego','drop-welder')
    #egotosid.actions[3].set_parsing([[' l',' ']])
    #egotosid.actions[3].set_function('addegowelderdrop')

    #sid.get_data()
    sidtoego = []
    for i, x in enumerate(egolist):
        sidtoego.append(Agent('ego'+x,'inspect','dropwelder','droppatch'))

        sidtoego[i].actions[0].set_identifiers('sid','inspect')
        sidtoego[i].actions[0].set_parsing([[' pn',' ']])
        sidtoego[i].actions[0].set_function('modifyinspectgoal')

        sidtoego[i].actions[1].set_identifiers('sid','drop-welder')
        sidtoego[i].actions[1].set_parsing([[' l',' '],[' w',' ']])
        sidtoego[i].actions[1].set_function('addwelderdrop')

        sidtoego[i].actions[2].set_identifiers('sid','drop-patch')
        sidtoego[i].actions[2].set_parsing([[' l',' '],[' pa', ' ']])
        sidtoego[i].actions[2].set_function('addpatchdrop')


    # Here the sidekick's patch list is parsed so that it can be updated correctly at each iteration.
    global patchset
    sep1 = sidempty.partition(';patchstart')
    sep2 = sep1[2].partition(';patchend')
    patchset = sep2[0]

    # Here the egobot problems are run for the first time.
    egoplan = []
    timeout = str(timeoutint)
    for i, problem in enumerate(egobotproblemfiles):
        egoplan.append(callplanner(planner,egodomain,problem,egobotplanfiles[i],timeout))

    # Here the first set of egobot plans are parsed.
    egobotplancompile = ''
    for i, output in enumerate(egoplan):
        egoplan[i], tempplanningtime = outputparser(output)
        planningtimetotal = planningtimetotal + tempplanningtime
        tempplanningtime = 0.0
        egobotplancompile = egobotplancompile + 'Egobot ' + egolist[i] + ' Plan:\n' + egoplan[i] + '\n\n'

    newsidproblem = sidempty

    egoscore = []
    for x in egolist:
        egoscore.append(0)

    welderdrops = []
    welderdroplocations = []
    welderdroptimes = []

    for i, plan in enumerate(egoplan):
        egoscore[i] = 0
        tempsuccesscheck = 1
        for action in egotosid.actions:
            parsedinfo, deadlines = planparser(plan,action)
            if deadlines:
                deadline = deadlines[-1]
            if any(info != [] for info in parsedinfo):
                function = action.function
                newsidproblem, score = eval(function+'(newsidproblem,parsedinfo,deadline)')
                egoscore[i] = egoscore[i]+score
                if action.identifiers[0] == 'sid':
                    tempsuccesscheck = 0
        tempwelders, templocations, temptimes = egowelderdropparser(plan)
        welderdrops = welderdrops + tempwelders
        welderdroplocations = welderdroplocations + templocations
        welderdroptimes = welderdroptimes + temptimes
        if tempsuccesscheck == 1:
            egosuccess[i] = 1
        print(str(egosuccess))

    if all(i == 1 for i in egosuccess):
        success = 1
        print(str(success))

    # Here the Sidekick plan compiling string is started
    sidplancompile = 'Sidekick Plan:\n'

    # Here the looping starts
    while success == 0:
        minscore = str(max(egoscore)-1)
        newsidproblem = modifysidekickgoal(newsidproblem,minscore)

        tempwelderdrops = []
        tempwelderdroplocations = []
        tempwelderdroptimes = []
        for i, welder in enumerate(welderdrops):
            if welder in tempwelderdrops:
                j = tempwelderdrops.index(welder)
                if float(welderdroptimes[i]) > float(tempwelderdroptimes[j]):
                    tempwelderdroplocations[j] = welderdroplocations[i]
                    tempwelderdroptimes[j] = welderdroptimes[i]
            else:
                tempwelderdrops.append(welder)
                tempwelderdroplocations.append(welderdroplocations[i])
                tempwelderdroptimes.append(welderdroptimes[i])
        welderdrops = tempwelderdrops
        welderdroplocations = tempwelderdroplocations
        welderdroptimes = tempwelderdroptimes

        adjustedwelderdroptimes = welderdroptimes
        for i, time in enumerate(welderdroptimes):
            adjustedwelderdroptimes[i] = str(float(time) - timeoffset)
            if float(adjustedwelderdroptimes[i]) < 0.01:
                adjustedwelderdroptimes[i] = '0.0'
        
        newsidproblem = addegowelderdrop(newsidproblem,welderdrops,welderdroplocations,adjustedwelderdroptimes)

        sidproblemfile = sidpt1 + iterstr + '.pddl'
        f = open(sidproblemfile,'x')
        f.write(newsidproblem) #currently missing using the score change function
        f.close()

        # Here the sidekick problem is run
        sidplanfile = sidpt2+iterstr+'.txt'
        timeout = str(timeoutint*4)
        sidplan = callplanner(planner,siddomain,sidproblemfile,sidplanfile,timeout)

        # Here the iteration number is increased
        iter = iter+1
        iterstr = str(iter)

        # Here the sidekick problem is parsed
        sidplan, tempplanningtime = outputparser(sidplan)
        planningtimetotal = planningtimetotal + tempplanningtime
        tempplanningtime = 0.0
        sidplancompile = sidplancompile + sidplan + '\n'
        sidtime, sidloc = endlocationparser(sidplan)
        timeoffsetold = timeoffset
        timeoffset = timeoffset+float(sidtime)
        egobotproblem = []
        for i, problemfile in enumerate(egobotproblemfiles):
            f = open(problemfile, 'r')
            egobotproblem.append(f.read())
            f.close()
            for action in sidtoego[i].actions:
                parsedinfo, deadlines = planparser(sidplan, action)
                if deadlines:
                    for j, time in enumerate(deadlines):
                        deadlines[j] = str(float(time)+timeoffsetold)
                if any(info != [] for info in parsedinfo):
                    function = action.function
                    egobotproblem[i] = eval(function+'(egobotproblem[i],parsedinfo,deadlines)')
            egobotproblem[i] = modifysidekicklocation(egobotproblem[i],sidloc,str(timeoffset))
            egobotproblemfiles[i] = egopt1+egolist[i]+egopt2+iterstr+'.pddl'
            egobotplanfiles[i] = egopt3+egolist[i]+egopt4+iterstr+'.txt'
            f = open(egobotproblemfiles[i], 'x')
            f.write(egobotproblem[i])
            f.close()
    
        # Here the egobot problems are run.
        timeout = str(timeoutint)
        for i, problem in enumerate(egobotproblemfiles):
            if egosuccess[i] == 0:
                egoplan[i] = callplanner(planner,egodomain,problem,egobotplanfiles[i],timeout)
            #else:
                #egoplan[i] = [] #removed because egosuccess is always(?) checked later down the line and this line messes with compilation
    
        # Here the egobot problems are parsed.
        egobotplancompile = ''
        for i, output in enumerate(egoplan):
            if egosuccess[i] == 0:
                egoplan[i], tempplanningtime = outputparser(output)
                planningtimetotal = planningtimetotal + tempplanningtime
                tempplanningtime = 0.0
            egobotplancompile = egobotplancompile + 'Egobot ' + egolist[i] + ' Plan:\n' + egoplan[i] + '\n\n'

        newsidproblem = sidempty

        welderdrops = []
        welderdroplocations = []
        welderdroptimes = []

        for i, plan in enumerate(egoplan):
            egoscore[i] = 0
            if egosuccess[i] == 0:
                tempsuccesscheck = 1
                for action in egotosid.actions:
                    parsedinfo, deadlines = planparser(plan,action)
                    if deadlines:
                        deadline = deadlines[-1]
                    deadline = str(float(deadline)-timeoffset)
                    #if parsedinfo != [[]]:
                    if any(info != [] for info in parsedinfo):
                        function = action.function
                        newsidproblem, score = eval(function+'(newsidproblem,parsedinfo,deadline)')
                        egoscore[i] = egoscore[i] + score
                        if action.identifiers[0] == 'sid':
                            tempsuccesscheck = 0
                tempwelders, templocations, temptimes = egowelderdropparser(plan)
                welderdrops = welderdrops + tempwelders
                welderdroplocations = welderdroplocations + templocations
                welderdroptimes = welderdroptimes + temptimes
                if tempsuccesscheck == 1:
                    egosuccess[i] = 1
            print(str(egosuccess))

        print(str(egosuccess))
        if all(i == 1 for i in egosuccess):
            success = 1
            print(str(success))
    
        newsidproblem = modifysidekickstart(newsidproblem,sidloc)

    # Here a final output file is generated
    f = open(finalplanfile, 'x')
    f.write(sidplancompile+'\n\n'+egobotplancompile+'\n\n'+str(planningtimetotal))

    # Here the planner is run for a single agent problem with up to twice the planning time total (I can compare to 100%, 110%, 120%, 150%, etc)
    singleagenttimeout = str(round(10*planningtimetotal))
    singleagentplan = callplanner(planner, fulldomain, fullproblemfile, fullplanfile, singleagenttimeout)

    return finalplanfile, planningtimetotal

#egolist = ['1', '2', '3', '4']
#egobotsidekick('04009031ring',egolist)