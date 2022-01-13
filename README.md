# egobots-and-sidekicks
A framework to extend standard planners to multi-agent planning problems.
The code is designed to run with the optic-cplex planner on Linux

Code for generating experiment scipt:
for v in $(seq -w 01 05); do for l in $(seq -w 01 04); do for e in $(seq -w 01 10); do echo "mkdir results_v${v}_e${e}_l${l}; python3 egosidtester.py $e $l; mv *star* results_v${v}_e${e}_l${l}/"; done; done; done > run_experiment... 

To run:
cat run_experiment... | sh

To run selected parts:
head run_experiment... -n 5 | sh
cat run_experiment... | grep e03 | sh
