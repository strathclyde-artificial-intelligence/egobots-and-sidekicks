# egobotsidekick.py
# This file performs the entire egobots sidekicks process for the inspect, weld, patch domain.
# This file takes an egobot domain, factored egobot problems, a sidekick domain, an empty sidekick problem, and a planner as input.
# This file generates files for each intermediate plan and problem.
# This file generates the final plans.

import os

# Here strings are defined which are used to find and create files.
egopt1 = 'egobot-'
egopt2 = '-problem-'
egopt3 = 'Egobot '
egopt4 = ' Iteration '
egolist = ['1','2','3','4']

sidpt1 = 'sidekick-problem-'
sidpt2 = 'Sidekick Iteration '

# Here the empty sidekick problem is named.
sidfileempty = 'sidekick-problem-empty.pddl'
f = open(sidfileempty,'r')
sidempty = f.read()
f.close()

# Here the domains are named.
egodomain = 'maintenance-domain.pddl'
siddomain = ''

# Here the planner is named.
planner = 'optic-cplex -n'

# Here the iteration counting variable and the success variable are made.
iter = 1
iterstr = str(iter)
success = 0
egosuccess = []
for x in egolist:
    egosuccess.append(0)

timeoffset = 0.0

# Here the egobot input file names are found.
egobotproblemfiles = []
egobotplanfiles = []
for x in egolist:
    egobotproblemfiles.append(egopt1+x+egopt2+iterstr+'.pddl')
    egobotplanfiles.append(egopt3+x+egopt4+iterstr+'.txt')

# Here the egobot problems are run for the first time.
egoplan = []
timeout = 'timeout 2 '
i = 0
for x in egobotproblemfiles:
    arg = timeout+'./'+planner+' '+egodomain+' '+x+' > '+egobotplanfiles[i]
    os.system(arg)
    f = open(egobotplanfiles[i],'r')
    tempstr1 = f.read()
    egoplan.append(tempstr1)
    f.close()
    i = i+1

# Here the first set of egobot plans are parsed.
egoinspdemands = [] # These are lists of lists.
egowelddemands = []
egoptchdemands = []
for i, x in enumerate(egoplan):
    tempstr1 = x.split('0.000:')
    tempstr2 = tempstr1[-1]
    tempstr3 = '0.000:'+tempstr2
    tempstr4 = tempstr3.splitlines()
    tempstr5 = []
    for y in tempstr4:
        if 'sid' in y:
            tempstr5.append(y)

    if tempstr5 == []:
        egosuccess[i] = 1
    else:
        tempstr6 = []
        for y in tempstr5:
            if 'inspect' in y:
                tempstr6.append(y)

        egoinspdemands.append(tempstr6)

        tempstr7 = []
        for y in tempstr5:
            if 'drop' in y:
                tempstr7.append(y)

        tempstr8 = []
        for y in tempstr7:
            if 'w' in y:
                tempstr8.append(y)

        egowelddemands.append(tempstr8)

        tempstr9 = []
        for y in tempstr7:
            if 'pa' in y:
                tempstr9.append(y)

        egoptchdemands.append(tempstr9)

if all(egosuccess): # In theory if there are any 0s in the list, it should return False
    success = 1

# Here the looping starts. There is not yet a way for this loop to end after a limit of iterations. There is not yet a way for this loop to recognise success.
while success == 0:
    # Here the inspect demands are formatted for the sidekick.
    tempstr2 = '\n'
    for x in egoinspdemands:
        tempstr1 = x[-1].partition(':')
        deadline = tempstr1[0]
        for y in x:
            tempstr3 = y.partition('pn')
            tempstr4 = tempstr3[2].partition(' ')
            panel = tempstr3[1]+tempstr4[0]
            tempstr5 = '\n'+'(= (ingoal '+panel+') 1)'+'\n'+'(is-not-inspected '+panel+')'+'\n'+'(at '+deadline+' (not (is-not-inspected '+panel+')))'
            tempstr2 = tempstr2 + tempstr5
    allinspdemandspddl = tempstr2

    # Here the empty sidekick problem is modified to include inspect requests.
    tempstr1 = sidempty.partition('(deadline-open)')
    tempstr2 = tempstr1[2].partition('(> (score) ')
    tempstr3 = tempstr2[2].partition('0')
    tempint1 = []
    for x in egoinspdemands:
        tempint1.append(len(x))
    minscore = max(tempint1) - 1
    minscorestr = str(minscore)
    tempstr4 = tempstr1[0]+tempstr1[1]+allinspdemandspddl+tempstr2[0]+minscorestr+tempstr2[2]
    sidproblem = tempstr4

    # Here the sidekick problem is saved as a file.
    sidfile = sidpt1+iterstr+'.pddl'
    f = open(sidfile,'x')
    f.write(sidproblem)
    f.close()

    # Here the sidekick problem is run.
    timeout = 'timeout 5 '
    sidplanfile = sidpt2+iterstr+'.txt'
    arg = timeout+'./'+planner+' '+siddomain+' '+sidfile+' > '+sidplanfile
    os.system(arg)
    f = open(sidplanfile, 'r')
    sidplan = f.read()
    f.close()

    # Here the iteration number is increased
    iter = iter+1
    iterstr = str(iter)

    # Here the sidekick problem is parsed for inspect actions.
    tempstr1 = sidplan.split('0.000:')
    tempstr2 = tempstr1[-1]
    tempstr3 = '0.000:'+tempstr2
    tempstr4 = tempstr3.splitlines()

    tempstr5 = []
    tempstr6 = []
    tempstr7 = []
    tempstr8 = []
    for x in tempstr4:
        if 'pn1' in x: # This if statement should be refined to handle n many egobots
            tempstr5.append(x)
        elif 'pn2' in x:
            tempstr6.append(x)
        elif 'pn3' in x:
            tempstr7.append(x)
        elif 'pn4' in x:
            tempstr8.append(x)
    
    tempstr9 = tempstr4[-1].partition(':')
    tempstr10 = tempstr9[0] # extracting the time the final action begins
    tempstr11 = tempstr4[-1].partition('l') # cutting at the sidekick's final location
    tempstr12 = tempstr11[2].partition(' ') # cutting off all data except location data
    tempstr13 = tempstr11[1]+tempstr12[0] # extracting final location

    sidplanend = str(float(tempstr10) + 1.0 + timeoffset) # add 1.0 because all actions take 1.0, this will need to be improved
    sidplanloc = tempstr13
    timeoffset = sidplanend

    egoactions = [tempstr5, tempstr6, tempstr7, tempstr8]
    egopanels = [[],[],[],[]]

    for i, x in enumerate(egoactions): # unsure if I have used enumerate correctly
        tempstr1 = []
        for y in x:
            tempstr2 = y.partition('pn')
            tempstr3 = tempstr2[2].partition(' ')
            tempstr1.append(tempstr2[1]+tempstr3[0])
        egopanels[i] = tempstr1

    # Here the egobot problems are adjusted
    for i, x in enumerate(egobotproblemfiles): # unsure if I have used enumerate correctly.2
        f = open(x, 'r')
        tempstr1 = f.read()
        f.close()
        
        tempstr2 = tempstr1.splitlines(True)
        tempstr3 = ''
        for y in tempstr2:
            if '(at sid ' in y:
                y = '(at '+sidplanend+' (at sid '+sidplanloc+')\n'
            for z in egopanels[i]:
                if z in y: # if panel is in line of egobot problem
                    if 'is-inspected' in x:
                        y = ';' + y
            tempstr3 = tempstr3 + y

        x = egopt1+egolist[i]+egopt2+iterstr+'.pddl'
        egobotplanfiles[i] = egopt3+egolist[i]+egopt4+iterstr+'.txt'

        f = open(x, 'x')
        f.write(x)
        f.close()
    
    # Here the egobot problems are run.
    timeout = 'timeout 2 '
    for i, x in enumerate(egobotproblemfiles): # unsure if I have used enumerate correctly.3
        if egosuccess[i] == 0:
            arg = timeout+'./'+planner+' '+egodomain+' '+x+' > '+egobotplanfiles[i]
            os.system(arg)
            f = open(egobotplanfiles[i],'r')
            tempstr1 = f.read()
            egoplan[i] = tempstr1
            f.close()
        else:
            egoplan[i] = []
    
    # Here the egobot problems are parsed.

    egoinspdemands = [] # These are lists of lists.
    egowelddemands = []
    egoptchdemands = []
    for i, x in enumerate(egoplan):
        tempstr1 = x.split('0.000:')
        tempstr2 = tempstr1[-1]
        tempstr3 = '0.000:'+tempstr2
        tempstr4 = tempstr3.splitlines()
        tempstr5 = []
        for y in tempstr4:
            if 'sid' in y:
                tempstr5.append(y)

        if tempstr5 == []:
            egosuccess[i] = 1
        else:
            tempstr6 = []
            for y in tempstr5:
                if 'inspect' in y:
                    tempstr6.append(y)

            egoinspdemands.append(tempstr6)

            tempstr7 = []
            for y in tempstr5:
                if 'drop' in y:
                    tempstr7.append(y)

            tempstr8 = []
            for y in tempstr7:
                if 'w' in y:
                    tempstr8.append(y)

            egowelddemands.append(tempstr8)

            tempstr9 = []
            for y in tempstr7:
                if 'pa' in y:
                    tempstr9.append(y)

            egoptchdemands.append(tempstr9)

    if all(egosuccess): # In theory if there are any 0s in the list, it should return False
        success = 1

# Here the script is done. I don't technically need any code here I guess (for now at least).