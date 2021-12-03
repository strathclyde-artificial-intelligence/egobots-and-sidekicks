# filecleaner.py
import os
def filecleaner(filecode):
    os.system('rm '+filecode+'sidekick-problem-empty-3.pddl')
    os.system('rm '+filecode+'full-problem.pddl')
    os.system('rm '+filecode+'Final-Plan.txt')
    os.system('rm '+filecode+'Single-Agent-Plan.txt')
    for i in range(1,200):
        os.system('rm '+filecode+'sidekick-problem-'+str(i)+'.pddl')
        os.system('rm '+filecode+'Sidekick-Iteration-'+str(i)+'.txt')
        for j in range(1,6):
            os.system('rm '+filecode+'egobot-'+str(j)+'-problem-'+str(i)+'.pddl')
            os.system('rm '+filecode+'Egobot-'+str(j)+'-Iteration-'+str(i)+'.txt')

filecleaner('05016041star')