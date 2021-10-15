# egobotsidekick.py
# This file performs the entire egobots sidekicks process for the inspect, weld, patch domain.
# This file takes an egobot domain, factored egobot problems, a sidekick domain, an empty sidekick problem, and a planner as input.
# This file generates files for each intermediate plan and problem.
# This file generates the final plans.
# This file can currently only handle inspect goals.
# This file requires that none of the auto-generated file names are already in use.

import os

# Here strings are defined which are used to find and create files.
egopt1 = 'egobot-'
egopt2 = '-problem-'
egopt3 = 'Egobot-'
egopt4 = '-Iteration-'
egolist = ['1','2','3','4']

sidpt1 = 'sidekick-problem-'
sidpt2 = 'Sidekick-Iteration-'

# Here the empty sidekick problem is named.
sidfileempty = 'sidekick-problem-empty-2.pddl'
f = open(sidfileempty,'r')
sidempty = f.read()
f.close()

# Here the domains are named.
egodomain = 'maintenance-domain.pddl'
siddomain = 'sidekick-domain-2.pddl'

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
timeout = 'timeout 10 '
i = 0
for x in egobotproblemfiles:
    f = open(egobotplanfiles[i],'x')
    f.close()
    arg = timeout+'./'+planner+' '+egodomain+' '+x+' > '+egobotplanfiles[i]
    os.system(arg)
    f = open(egobotplanfiles[i],'r')
    tempstr1 = f.read()
    egoplan.append(tempstr1)
    f.close()
    i = i+1

# Here the first set of egobot plans are parsed.
egodemands = [] # These are lists of lists.
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
            if 'inspect' or 'drop' in y:
                tempstr6.append(y)

        egodemands.append(tempstr6)

# Add parsing for where welders and patches end up

if all(egosuccess): # In theory if there are any 0s in the list, it should return False
    success = 1

# Here the looping starts. There is not yet a way for this loop to end after a limit of iterations.
while success == 0:
    # Here the inspect demands are formatted for the sidekick.
    tempstr2 = '\n'
    for x in egodemands:
        tempstr1 = x[-1].partition(':')
        deadline = tempstr1[0]
        for y in x:
            if 'inspect' in y:
                tempstr3 = y.partition('pn')
                tempstr4 = tempstr3[2].partition(' ')
                panel = tempstr3[1]+tempstr4[0]
                tempstr5 = '\n'+'(= (ingoal '+panel+') 1)'+'\n'+'(is-not-inspected '+panel+')'+'\n'+'(at '+deadline+' (not (is-not-inspected '+panel+')))'
                tempstr2 = tempstr2 + tempstr5
            elif 'drop' in y:
                if 'w' in y:
                    tempstr3 = y.partition(' l') # partition at location
                    tempstr4 = tempstr3[2].partition(')')
                    droplocation = 'l'+tempstr4[0]
                    tempstr5 = '\n'+'(= (wegoal '+droplocation+') 10)'+'\n'+'(welder-drop-needed '+droplocation+')'+'\n'+'(at '+deadline+' (not (welder-drop-needed '+droplocation+')))'
                if 'pa' in y: #currently just same as welder, must be updated
                    tempstr3 = y.partition(' l') # partition at location
                    tempstr4 = tempstr3[2].partition(')')
                    droplocation = 'l'+tempstr4[0]
                    tempstr5 = '\n'+'(= (wegoal '+droplocation+') 10)'+'\n'+'(welder-drop-needed '+droplocation+')'+'\n'+'(at '+deadline+' (not (welder-drop-needed '+droplocation+')))'
    alldemandspddl = tempstr2

    # Add welder and patch demands here.

    # Here the empty sidekick problem is modified to include inspect requests.
    tempstr1 = sidempty.partition('(deadline-open)')
    tempstr2 = tempstr1[2].partition('(> (score) ')
    tempstr3 = tempstr2[2].partition('0')
    tempint1 = []
    for x in egodemands:
        tempint1.append(len(x))
    minscore = max(tempint1) - 1
    minscorestr = str(minscore)
    tempstr4 = tempstr1[0]+tempstr1[1]+alldemandspddl+tempstr2[0]+tempstr2[1]+tempstr3[0]+minscorestr+tempstr3[2]
    sidproblem = tempstr4

    # Here the sidekick problem is saved as a file.
    sidfile = sidpt1+iterstr+'.pddl'
    f = open(sidfile,'x')
    f.write(sidproblem)
    f.close()

    # Here the sidekick problem is run.
    timeout = 'timeout 20 '
    sidplanfile = sidpt2+iterstr+'.txt'
    f = open(sidplanfile, 'x')
    f.close()
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
    tempstr3b = tempstr3.split('[1.000]\n')
    tempstr3c = ''
    for x in tempstr3b:
        if ': (' in x:
            tempstr3c = tempstr3c + '\n'+ x + '[1.000]'
    #print('tempstr3c is: ' +tempstr3c)
    tempstr4 = tempstr3c.splitlines()

    tempstr5 = []
    tempstr6 = []
    tempstr7 = []
    tempstr8 = []
    for x in tempstr4:
        if 'pn1' in x: # This if statement should be refined to handle n many egobots
            # tempdict['pn1'] = [] # if its not created yet.
            # tempdict['pn1'].append(x)
            tempstr5.append(x)
        elif 'pn2' in x:
            tempstr6.append(x)
        elif 'pn3' in x:
            tempstr7.append(x)
        elif 'pn4' in x:
            tempstr8.append(x)
    
    #print('tempstr5 is: ')
    #for x in tempstr5:
    #    print(x)
    #print('tempstr6 is: ')
    #for x in tempstr6:
    #    print(x)
    #print('tempstr7 is: ')
    #for x in tempstr7:
    #    print(x)
    #print('tempstr8 is: ')
    #for x in tempstr8:
    #    print(x)

    tempstr9 = tempstr4[-1].partition(':')
    #print('tempstr9 is: ')
    #for x in tempstr9:
    #    print(x)
    tempstr10 = tempstr9[0] # extracting the time the final action begins
    #print('tempstr10 is: ' + tempstr10)
    tempstr11 = tempstr4[-1].partition('l') # cutting at the sidekick's final location
    #print('tempstr11 is: ')
    #for x in tempstr11:
    #    print(x)
    tempstr12 = tempstr11[2].partition(' ') # cutting off all data except location data
    #print('tempstr12 is: ')
    #for x in tempstr12:
    #    print(x)
    tempstr13 = tempstr11[1]+tempstr12[0] # extracting final location
    #print('tempstr13 is: ' + tempstr13)

    sidplanend = str(float(tempstr10) + 1.0 + timeoffset) # add 1.0 because all actions take 1.0, this will need to be improved
    #print('sidplanend is: ' + sidplanend)
    sidplanloc = tempstr13
    timeoffset = float(sidplanend)

    egoactions = [tempstr5, tempstr6, tempstr7, tempstr8]
    egopanels = [[],[],[],[]]

    for i, x in enumerate(egoactions):
        tempstr1 = []
        for y in x:
            tempstr2 = y.partition('pn')
            tempstr3 = tempstr2[2].partition(' ')
            tempstr1.append(tempstr2[1]+tempstr3[0])
        egopanels[i] = tempstr1
        print('egopanels ' + str(i) + ' is: ')
        for z in egopanels[i]:
            print(z)
    
    # Add parsing for weld drops and patch drops

    # Here the egobot problems are adjusted
    for i, x in enumerate(egobotproblemfiles):
        f = open(x, 'r')
        tempstr1 = f.read()
        f.close()
        print('tempstr1 is: ' + tempstr1)
        
        tempstr2 = tempstr1.splitlines(True)
        tempstr3 = ''
        for y in tempstr2:
            if '(at sid ' in y:
                y = '(at '+sidplanend+' (at sid '+sidplanloc+')\n'
                print('Line changed to:' + y)
            for z in egopanels[i]:
                if z in y: # if panel is in line of egobot problem
                    if 'is-inspected' in y:
                        y = ';' + y
                        print('Line changed to:' + y)
            tempstr3 = tempstr3 + y

        print('tempstr3 is ' + tempstr3)

        egobotproblemfiles[i] = egopt1+egolist[i]+egopt2+iterstr+'.pddl'
        egobotplanfiles[i] = egopt3+egolist[i]+egopt4+iterstr+'.txt'

        f = open(egobotproblemfiles[i], 'x')
        f.write(tempstr3)
        f.close()
    
    # Here the egobot problems are run.
    timeout = 'timeout 10 '
    for i, x in enumerate(egobotproblemfiles):
        if egosuccess[i] == 0:
            f = open(egobotplanfiles[i],'x')
            f.close()
            arg = timeout+'./'+planner+' '+egodomain+' '+x+' > '+egobotplanfiles[i]
            os.system(arg)
            f = open(egobotplanfiles[i],'r')
            tempstr1 = f.read()
            egoplan[i] = tempstr1
            f.close()
        else:
            egoplan[i] = []
    
    # Here the egobot problems are parsed.
    egodemands = [] # These are lists of lists.
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
                if 'inspect' or 'drop' in y:
                    tempstr6.append(y)

            egodemands.append(tempstr6)

    if all(egosuccess): # In theory if there are any 0s in the list, it should return False
        success = 1

# Could add a message here about reaching success.