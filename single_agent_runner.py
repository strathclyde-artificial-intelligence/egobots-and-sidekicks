#single_agent_runner.py
import os

timeout = '1800'
planner = 'optic-cplex'

experimentfiles = [f for f in os.listdir() if "run_experiment" in f]
experimentfiles.remove("run_experiment_v1-5_e3-20_l3-15_pruned")
experimentfiles.remove("run_experiment_v5_e10_l4")
experimentstr = [ [] for _ in range(len(experimentfiles)) ]
for i,x in enumerate(experimentfiles):
    with open(x) as ff:
        experimentstr[i] = ff.readlines()

dirs = [f for f in os.listdir() if "results_v" in f]

for dir in dirs:
    print(dir)
    orderchecker = [ [] for _ in range(len(experimentstr)) ]
    filefound = 0
    for i, list in enumerate(experimentstr):
        orderchecker[i] = [j for j,f in enumerate(list) if dir in f]
        orderchecker[i][:0] = [i]
        if len(orderchecker[i]) > 1:
            filefound = 1
    
    testcomplete = 1 # if the next loop bugs and doesn't set a value, the value of 1 is a better default than using the previous iteration's value
    if filefound == 0:
        testcomplete = 1 # returns a go-ahead if I can't find which run_experiment file created this result
        print("file not found")
    else:
        for pos in orderchecker: 
            if len(pos) > 1: # iterates through all the times this results folder can be found in run_experiment (should only be once)
                if pos[1] < len(experimentstr[pos[0]])-1: # checks that this results folder wasn't generated by the last line
                    nextexperiment = experimentstr[pos[0]][pos[1]+1]
                    if any(dir2 in nextexperiment for dir2 in dirs):
                        testcomplete = 1
                        print("next experiment found")
                        print(nextexperiment)
                    else:
                        testcomplete = 0
                        print("next experiment not found")
                else:
                    testcomplete = 1
                    print("final experiment")
    
    if testcomplete == 1:
        single_agent_file_list = [f for f in os.listdir(dir) if "Single" in f]
        if single_agent_file_list == []:
            fullproblemfile = [f for f in os.listdir(dir) if "full-problem" in f][0]
            filesep = fullproblemfile.partition('star')
            filecode = filesep[0]+filesep[1]
            fullplanfile = filecode+'Single-Agent-Plan.txt'
            fulldomain = 'maintenance-domain-2.pddl'

            fullproblemfile = dir + "/" + fullproblemfile
            fullplanfile = dir + "/" + fullplanfile

            f = open(fullplanfile,'x')
            f.close()

            arg = 'timeout '+timeout+' ./'+planner+' '+fulldomain+' '+fullproblemfile+' > '+fullplanfile
            print(arg)
            os.system(arg)
