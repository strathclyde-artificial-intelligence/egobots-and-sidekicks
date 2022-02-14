# egobots-and-sidekicks

A framework to extend standard planners to multi-agent planning problems.
The code is designed to run with the optic-cplex planner on Linux.

### Setup

The following is a list of which files must be where for the framework to function. These files are all in the correct place in the GitHub, except for optic-cplex which is not included on the GitHub.
 - You must have optic-cplex in the same folder as egobotsidekickv2function.py for egobotsidekickv2function.py to call on the planner correctly.
 - You must have sidekick-domain-3.pddl, egobot-domain.pddl, and maintenance-domain-2-welderless.py in the same folder as egobotsidekickv2function.py for egobotsidekickv2function.py to call on domains correctly.
 - You must have egobotsidekickv2function.py and egosidproblemgenerator.py in the same folder as egosidtester.py for egosidtester.py to call on them.

### Instructions

The following line will call on egosidtester.py to create and solve a simple problem:

```bash
python3 egosidtester.py 04 04
```

This will solve the multi-agent problem first, then it will give the single agent half an hour to find the best solution it can for the same problem. To modify the timeout on the single agent, change the string `singleagenttimeout` on line 634 of egobotsidekickv2function.py.

The files generated during planning will all be generated in the same folder as egobotsidekickv2function.py. These will all start with the string 04016041star. I suggest making a folder to store all these files, but they shouldn't be moved until the planning is complete. The files should include the following:

| **File**                                  | **Description**                                                                                                                  |
|-------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|
| 04016041staregobot-XX-problem-Y.pddl      | problem files for each Egobot planning agent where XX is the Egobot's number and Y is the planning iteration                     |
| 04016041starEgobot-XX-Iteration-Y.txt     | plan file for each Egobot planning agent where XX is the Egobot's number and Y is the planning iteration                         |
| 04016041starsidekick-problem-empty-3.pddl | a template problem file for the Sidekick which is used to generate later Sidekick problems                                       |
| 04016041starsidekick-problem-Y.pddl       | problem files for the Sidekick where Y is the planning iteration                                                                 |
| 04016041starSidekick-Iteration-Y.pddl     | plan files for the Sidekick where Y is the planning iteration                                                                    |
| 04016041starFinal-Plan.txt                | collated plan file, the final plans to be executed by all agents (note: the Sidekick action start times reset in each iteration) |
| 04016041starSingle-Agent-Problem.txt      | the full problem file                                                                                                            |
| 04016041starSingle-Agent-Plan.txt         | the single agent plan file                                                                                                       |

The string '04016041star' refers to number of egobots '04', number of goals per egobot '016', number of locations per egobot '04', number of sidekicks '1', and the shape of the problem locations 'star'.

Code for generating experiment scipt (bash)
```bash
for v in $(seq -w 01 05); do for l in $(seq -w 01 04); do for e in $(seq -w 01 10); do echo "mkdir results_v${v}_e${e}_l${l}; python3 egosidtester.py $e $l; mv *star* results_v${v}_e${e}_l${l}/"; done; done; done > run_experiment... 
```

To run:
```bash
cat run_experiment... | sh
```

To run selected parts:
```bash
head run_experiment... -n 5 | sh
cat run_experiment... | grep e03 | sh
```
