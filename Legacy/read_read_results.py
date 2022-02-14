#read_read_results.py
#don't judge the name I'm tired

#import numpy, but i don't have numpy
import copy

f = open('tempresults.txt','r')
results = f.read()
f.close()

resultlines = results.splitlines()
resultcells = resultlines[1:]
for i,line in enumerate(resultcells):
    resultcells[i] = resultcells[i].split(',')

egolocformat = [['egobots\\locations',3,4,5,6,7,8,9,10,11,12,13],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20]]
for i,line in enumerate(egolocformat):
    if i > 0:
        for j in range(11):
            egolocformat[i].append(0)

frameworktime = copy.deepcopy(egolocformat)
frameworkattempts = copy.deepcopy(egolocformat)
#print(frameworkattempts)
frameworksuccess = copy.deepcopy(egolocformat)

for line in resultcells:
    egobots = int(line[2])
    locations = int(line[3])
    #print('nextcell')
    row = egobots-2
    #print(row)
    column = locations-2
    #print(column)
    frameworkattempts[row][column] = frameworkattempts[row][column] + 1
    #print(frameworkattempts[row][column])
    if line[5] != '-':
        if float(line[5]) < 1800:
            frameworktime[row][column] = (float(frameworktime[row][column])*float(frameworksuccess[row][column]) + float(line[5]))/(float(frameworksuccess[row][column])+float(1))
            frameworksuccess[row][column] += 1

frameworktimeprint = 'Framework Average Time:\n'
for row in range(len(egolocformat)):
    temprowstr = ''
    for column in range(len(egolocformat[0])):
        temprowstr = temprowstr + str(frameworktime[row][column]) + ','
    
    frameworktimeprint = frameworktimeprint + temprowstr[:-1] + '\n'

print(frameworktimeprint)

frameworkattemptprint = 'Framework Attempts:\n'
for row in range(len(egolocformat)):
    temprowstr = ''
    for column in range(len(egolocformat[0])):
        temprowstr = temprowstr + str(frameworkattempts[row][column]) + ','
    
    frameworkattemptprint = frameworkattemptprint + temprowstr[:-1] + '\n'

print(frameworkattemptprint)

frameworksuccessprint = 'Framework Successful Attempts'
for row in range(len(egolocformat)):
    temprowstr = ''
    for column in range(len(egolocformat[0])):
        temprowstr = temprowstr + str(frameworksuccess[row][column]) + ','
    
    frameworksuccessprint = frameworksuccessprint + temprowstr[:-1] + '\n'

print(frameworksuccessprint)

singleagenttime = copy.deepcopy(egolocformat)
singleagentattempts = copy.deepcopy(egolocformat)
singleagentsuccess = copy.deepcopy(egolocformat)

for line in resultcells:
    egobots = int(line[2])
    locations = int(line[3])
    row = egobots-2
    column = locations-2
    if line[7] != 'no single agent plan':
        singleagentattempts[row][column] = frameworkattempts[row][column] + 1
        if line[7] != '-' or (line[9] != '-' and line[9] != 'no welderless agent plan'):
            #print(line[7])
            #print(line[7].isnumeric())
            if line[7][0].isnumeric():
                print(line[7])
                print(line[7][0].isnumeric())
                mintime = float(line[7])
                if line[9][0].isnumeric():
                    mintime = min(float(line[7]),float(line[9]))
            elif line[9][0].isnumeric():
                mintime = float(line[9])
            else:
                mintime = ''
            if type(mintime) == float:
                print(mintime)
                singleagenttime[row][column] = (float(singleagenttime[row][column])*float(singleagentsuccess[row][column]) + mintime)/(float(singleagentsuccess[row][column])+float(1))
                singleagentsuccess[row][column] += 1

singleagenttimeprint = 'Single Agent Average Time:\n'
for row in range(len(egolocformat)):
    temprowstr = ''
    for column in range(len(egolocformat[0])):
        temprowstr = temprowstr + str(singleagenttime[row][column]) + ','
    
    singleagenttimeprint = singleagenttimeprint + temprowstr[:-1] + '\n'

print(singleagenttimeprint)

singleagentattemptprint = 'Single Agent Attempts:\n'
for row in range(len(egolocformat)):
    temprowstr = ''
    for column in range(len(egolocformat[0])):
        temprowstr = temprowstr + str(singleagentattempts[row][column]) + ','
    
    singleagentattemptprint = singleagentattemptprint + temprowstr[:-1] + '\n'

print(singleagentattemptprint)

singleagentsuccessprint = 'Single Agent Successful Attempts:\n'
for row in range(len(egolocformat)):
    temprowstr = ''
    for column in range(len(egolocformat[0])):
        temprowstr = temprowstr + str(singleagentsuccess[row][column]) + ','
    
    singleagentsuccessprint = singleagentsuccessprint + temprowstr[:-1] + '\n'

print(singleagentsuccessprint)

maxcomplexityformat = [['egobots','framework max location','single agent max location'],[3,'N/A','N/A'],[4,'N/A','N/A'],[5,'N/A','N/A'],[6,'N/A','N/A'],[7,'N/A','N/A'],[8,'N/A','N/A'],[9,'N/A','N/A'],[10,'N/A','N/A'],[11,'N/A','N/A'],[12,'N/A','N/A'],[13,'N/A','N/A'],[14,'N/A','N/A'],[15,'N/A','N/A'],[16,'N/A','N/A'],[17,'N/A','N/A'],[18,'N/A','N/A'],[19,'N/A','N/A'],[20,'N/A','N/A']]

halfhourmaxcomplexity = copy.deepcopy(maxcomplexityformat)

for i, resultrow in enumerate(halfhourmaxcomplexity[1:]):
    maxloc = 0
    for j, timecell in enumerate(frameworksuccess[i+1][1:]):
        if timecell > 0:
            maxloc = j+3
    if maxloc > 0:
        halfhourmaxcomplexity[i+1][1] = int(maxloc) #if there is no function here, would the result be locked into the value of maxloc and change as maxloc changes?
    maxloc = 0
    for j, timecell in enumerate(singleagentsuccess[i+1][1:]):
        if timecell > 0:
            maxloc = j+3
    if maxloc > 0:
        halfhourmaxcomplexity[i+1][2] = int(maxloc)

halfhourmaxcomplexityprint = 'Maximum Locations Per Egobot by Egobots in 30 Minutes:\n'
for row in range(len(halfhourmaxcomplexity)):
    temprowstr = ''
    for column in range(len(halfhourmaxcomplexity[0])):
        temprowstr = temprowstr + str(halfhourmaxcomplexity[row][column]) + ','
    
    halfhourmaxcomplexityprint = halfhourmaxcomplexityprint + temprowstr[:-1] + '\n'

print(halfhourmaxcomplexityprint)