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

def addinspectrequest(file, panels, deadline):
    sep1 = file.partition(';inspectrequests') # this comment must be added in the :init section of the empty sidekick problem
    newfile = sep1[0]+sep1[1]
    for panel in panels:
        newfile = newfile + '\n'+'(= (ingoal '+panel+') 1)'+'\n'+'(is-not-inspected '+panel+')'+'\n'+'(at '+deadline+' (not (is-not-inspected '+panel+')))'
    newfile = newfile+sep1[2]
    return newfile

def addwelderrequest(file, droplocations, deadline):
    sep1 = file.partition(';welderdroprequests') # this comment must be added in the :init section of the empty sidekick problem
    newfile = sep1[0]+sep1[1]
    for droplocation in droplocations:
        newfile = newfile + '\n'+'(= (wegoal '+droplocation+') 10)'+'\n'+'(welder-drop-needed '+droplocation+')'+'\n'+'(at '+deadline+' (not (welder-drop-needed '+droplocation+')))'
    newfile = newfile+sep1[2]
    return newfile

def addpatchrequest(file, droplocations, deadline):
    newfile = file
    return newfile

def addegowelderdrop(file, locations, times):
    newfile = file
    return newfile

def modifyinspectgoal(file, panels, placeholder): # this function takes in a list of all the panels, if you do only one panel at a time it will be slower
    sep1 = file.partition(';goalstart') # this comment must be located at the start of the egobot's goals
    sep2 = sep1[2].partition(';goalend') # this comment must be located at the end of the egobot's goals
    sep3 = sep2[0].splitlines()
    newgoals = ''
    for line in sep3:
        if any(panel in line for panel in panels):
            newgoals = newgoals + '\n'+';'+line
        else:
            newgoals = newgoals + '\n'+line
    newfile = sep1[0]+sep1[1]+newgoals+'\n'+sep2[1]+sep2[2]
    return newfile

def addwelderdrop(file, placeholder, placeholder2):
    newfile = file
    return newfile

def addpatchdrop(file, placeholder, placeholder2):
    newfile = file
    return newfile

def modifysidekicklocation(file, sidloc, sidtime):
    sep1 = file.partition(';sidlocstart') # this comment must be placed before the sidekick's starting location in the egobot problem file
    sep2 = sep1[2].partition(';sidlocend') # this comment must be placed after
    newfile = sep1[0]+sep1[1]+ '\n'+'(at '+sidtime+' (at sid '+sidloc+'))\n'+sep2[1]+sep2[2]
    return newfile

def modifysidekickstart(file, sidloc):
    sep1 = file.partition(';sidlocstart') # this comment must be placed before the sidekick's starting location in the empty sidekick problem file
    sep2 = sep1[2].partition(';sidlocend') # this comment must be placed after
    newfile = sep1[0]+sep1[1]+ '\n'+' (at sid '+sidloc+')\n'+sep2[1]+sep2[2]
    return newfile

def modifysidekickgoal(file, minscore): # minscore must be a string
    sep1 = file.partition(';goalstart')
    sep2 = sep1[2].partition(';goalend')
    newfile = sep1[0]+sep1[1]+'\n'+'(> (score) '+minscore+')'+'\n'+sep2[1]+sep2[2]
    return newfile

# These are the parser functions

def outputparser(file): # this function extracts a plan from a planner's output log
    splitbyplan = file.split('[0.000]:')
    lastplan = splitbyplan[-1]
    lastplanlines = lastplan.splitlines()
    plan = ''
    for line in lastplanlines:
        if ': (' in line:
            plan = plan + '\n' + line
    return plan

def planparser(plan, action): # this function parses a plan string for information contained in the parsing pairs on lines identified by identifiers
    planlines = plan.splitlines()
    identifiers = action.identifiers
    parsing = action.parsing
    relevantlines = []
    keyinfo = []
    keyinfo.append([])
    for line in planlines:
        if all(key in line for key in identifiers): # the line must contain every identifier string to be accepted
            relevantlines.append(line)
    for line in relevantlines:
        for i, pair in enumerate(parsing): # parsing is a list of lists of strings, each list of strings has two strings
            sep1 = line.partition(pair[0]) # cut off the part of the line before the info to be parsed
            sep2 = sep1[2].partition(pair[1]) # cut off the part of the line after the info to be parsed
            keydatum = sep1[1]+sep2[0]+sep2[1] # combine the parsing strings with the contained string
            keyinfo[i].append(keydatum.strip()) # the spaces used in the parsing strings are removed by the .strip()
    if relevantlines:
        lastrelevantline = relevantlines[-1]
        timesep1 = lastrelevantline.partition(':') # extract starting time of the last line
        #timesep2a = timesep1[2].partition(' [') # extract duration of the last line
        #timesep2b = timesep2a[2].partition(']') # trim square bracket off the duration
        lastlinestart = timesep1[0]
        #lastlinedur = timesep2b[0]
        deadline = str(float(lastlinestart)+0.005)#+float(lastlinedur))
        # 0.005 second buffer has been added due to an error which occured when the sidekick had only one request to deal with and that request was at its starting location, thus having a deadline of 0.001 seconds
    else:
        deadline = 0
    return keyinfo, deadline # a list of lists of strings such as panels and a string giving the start time of the last request

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
egopt1 = '21egobot-'
egopt2 = '-problem-'
egopt3 = '21Egobot-'
egopt4 = '-Iteration-'
egolist = ['1','2','3','4']

sidpt1 = '21sidekick-problem-'
sidpt2 = '21Sidekick-Iteration-'

# Here the empty sidekick problem is named.
sidfileempty = 'sidekick-problem-empty-3.pddl'
f = open(sidfileempty,'r')
sidempty = f.read()
f.close()

# Here the domains are named.
egodomain = 'maintenance-domain-2.pddl'
siddomain = 'sidekick-domain-3.pddl'

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

# Here the egobot input file names are found.
egobotproblemfiles = []
egobotplanfiles = []
for egobotnum in egolist:
    egobotproblemfiles.append(egopt1+egobotnum+egopt2+iterstr+'.pddl')
    egobotplanfiles.append(egopt3+egobotnum+egopt4+iterstr+'.txt')

# Here the agents and actions are created.
egotosid = Agent('sid','inspect','dropwelder','droppatch','egodropwelder')

egotosid.actions[0].set_identifiers('sid','inspect')
egotosid.actions[0].set_parsing([[' pn',' ']])
egotosid.actions[0].set_function('addinspectrequest')

egotosid.actions[1].set_identifiers('sid','drop-welder')
egotosid.actions[1].set_parsing([[' l',' ']])
egotosid.actions[1].set_function('addwelderrequest')

egotosid.actions[2].set_identifiers('sid','drop-patch')
egotosid.actions[2].set_parsing([[' l',' ']])
egotosid.actions[2].set_function('addpatchrequest')

egotosid.actions[3].set_identifiers('ego','drop-welder')
egotosid.actions[3].set_parsing([[' l',' ']])
egotosid.actions[3].set_function('addegowelderdrop')

#sid.get_data()
sidtoego = []
for i, x in enumerate(egolist):
    sidtoego.append(Agent('ego'+x,'inspect','dropwelder','droppatch'))

    sidtoego[i].actions[0].set_identifiers('sid','inspect')
    sidtoego[i].actions[0].set_parsing([[' pn',' ']])
    sidtoego[i].actions[0].set_function('modifyinspectgoal')

    sidtoego[i].actions[1].set_identifiers('sid','drop-welder')
    sidtoego[i].actions[1].set_parsing([[' l',' ']])
    sidtoego[i].actions[1].set_function('addwelderdrop')

    sidtoego[i].actions[2].set_identifiers('sid','drop-patch')
    sidtoego[i].actions[2].set_parsing([[' l',' ']])
    sidtoego[i].actions[2].set_function('addpatchdrop')

# Here the egobot problems are run for the first time.
egoplan = []
timeout = '10'
for i, problem in enumerate(egobotproblemfiles):
    egoplan.append(callplanner(planner,egodomain,problem,egobotplanfiles[i],timeout))

# Here the first set of egobot plans are parsed.
for i, output in enumerate(egoplan):
    egoplan[i] = outputparser(output)

newsidproblem = sidempty

for i, plan in enumerate(egoplan):
    tempsuccesscheck = 1
    for action in egotosid.actions:
        parsedinfo, deadline = planparser(plan,action)
        if parsedinfo != [[]]:
            function = action.function
            newsidproblem = eval(function+'(newsidproblem,parsedinfo[0],deadline)') # the 0 is a temporary workaround because parsedinfo is a list of lists
            tempsuccesscheck = 0
    if tempsuccesscheck == 1:
        egosuccess[i] = 1
    print(str(egosuccess))

if all(i == 1 for i in egosuccess):
    success = 1
    print(str(success))

# Here the looping starts
while success == 0:
    sidproblemfile = sidpt1 + iterstr + '.pddl'
    f = open(sidproblemfile,'x')
    f.write(newsidproblem) #currently missing using the score change function
    f.close()

    # Here the sidekick problem is run
    sidplanfile = sidpt2+iterstr+'.txt'
    timeout = '20'
    sidplan = callplanner(planner,siddomain,sidproblemfile,sidplanfile,timeout)

    # Here the iteration number is increased
    iter = iter+1
    iterstr = str(iter)

    # Here the sidekick problem is parsed
    sidplan = outputparser(sidplan)
    sidtime, sidloc = endlocationparser(sidplan)
    timeoffset = timeoffset+float(sidtime)
    egobotproblem = []
    for i, problemfile in enumerate(egobotproblemfiles):
        f = open(problemfile, 'r')
        egobotproblem.append(f.read())
        f.close()
        for action in sidtoego[i].actions:
            parsedinfo, redundant = planparser(sidplan, action)
            if parsedinfo != [[]]:
                function = action.function
                egobotproblem[i] = eval(function+'(egobotproblem[i],parsedinfo[0],deadline)')
        egobotproblem[i] = modifysidekicklocation(egobotproblem[i],sidloc,str(timeoffset))
        egobotproblemfiles[i] = egopt1+egolist[i]+egopt2+iterstr+'.pddl'
        egobotplanfiles[i] = egopt3+egolist[i]+egopt4+iterstr+'.txt'
        f = open(egobotproblemfiles[i], 'x')
        f.write(egobotproblem[i])
        f.close()
    
    # Here the egobot problems are run.
    timeout = '10'
    for i, problem in enumerate(egobotproblemfiles):
        if egosuccess[i] == 0:
            egoplan[i] = callplanner(planner,egodomain,problem,egobotplanfiles[i],timeout)
        else:
            egoplan[i] = []
    
    # Here the egobot problems are parsed.
    for i, output in enumerate(egoplan):
        if egosuccess[i] == 0:
            egoplan[i] = outputparser(output)

    newsidproblem = sidempty

    for i, plan in enumerate(egoplan):
        if egosuccess[i] == 0:
            tempsuccesscheck = 1
            for action in egotosid.actions:
                parsedinfo, deadline = planparser(plan,action)
                deadline = str(float(deadline)-timeoffset)
                if parsedinfo != [[]]:
                    function = action.function
                    newsidproblem = eval(function+'(newsidproblem,parsedinfo[0],deadline)') # the 0 is a temporary workaround because parsedinfo is a list of lists
                    tempsuccesscheck = 0
            if tempsuccesscheck == 1:
                egosuccess[i] = 1
            print(str(egosuccess))

    print(str(egosuccess))
    if all(i == 1 for i in egosuccess):
        success = 1
        print(str(success))
    
    newsidproblem = modifysidekickstart(newsidproblem,sidloc)