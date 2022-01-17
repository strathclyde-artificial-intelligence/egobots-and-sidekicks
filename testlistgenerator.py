# testlistgenerator.py
import os


def addtest(testliststr,version,loc,ego):
    testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+' v'+str(version)+'; mv v'+str(version)+'* results_v'+str(version)+'_e'+ego+'_l'+loc+';\n'
    return testliststr

testliststr = ''
for version in range(10,11): #remember the end is 1 less than the second number
    loc = '03'
    for ego in range(3,21):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)
    loc = '04'
    for ego in range(3,14):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '05'
    for ego in range(3,11):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '06'
    for ego in range(3,9):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '07'
    for ego in range(3,7):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '08'
    for ego in range(3,6):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '09'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '10'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '11'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '12'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    
    loc = '13'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr = addtest(testliststr,version,loc,ego)    

f = open('run_experiment_v10_e3-20_l3-15_pruned', 'w')
f.write(testliststr)
f.close()