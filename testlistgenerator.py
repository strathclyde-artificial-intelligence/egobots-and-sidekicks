# testlistgenerator.py
import os


testliststr = ''
for version in range(1,6): #remember this is 1 to 5
    loc = '03'
    for ego in range(3,21):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '04'
    for ego in range(3,14):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '05'
    for ego in range(3,11):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '06'
    for ego in range(3,9):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '07'
    for ego in range(3,7):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '08'
    for ego in range(3,6):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '09'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '10'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '11'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '12'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'
    loc = '13'
    for ego in range(3,5):
        ego = str(ego)
        if len(ego) == 1:
            ego = '0'+ego
        testliststr=testliststr+'mkdir results_v'+str(version)+'_e'+ego+'_l'+loc+'; python3 egosidtester.py '+ego+' '+loc+'; mv *star* results_v'+str(version)+'_e'+ego+'_l'+loc+'\n'

f = open('run_experiment_v1-5_e3-20_l3-15_pruned', 'w')
f.write(testliststr)
f.close()