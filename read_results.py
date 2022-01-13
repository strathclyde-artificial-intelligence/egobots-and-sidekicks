from os import listdir

print("setup,variant,egobot,locations,goals,framework_time,framework_plan_duration,single_agent_time,single_agent_duration")

dirs = [f for f in listdir() if "results_v" in f]
for dir in dirs:

    print (dir, end=",")
    single_agent_file = [f for f in listdir(dir) if "Single" in f][0]
    final_plan = [f for f in listdir(dir) if "Final" in f][0]

    tokens = dir.split("_")
    variant = tokens[1][1:]
    egobots = tokens[2][1:]
    locations = tokens[3][1:]
    goals = int(locations)*4

    print(variant+","+egobots+","+locations+","+str(goals),end=",")

    # framework
    cost = "-"
    time = "-"
    with open(dir+"/"+final_plan) as ff:
        lines = ff.readlines()
        state = 0 # reading sidekick plan
        plan_offset = 0.0
        for line in lines:
            if "Egobot" in line: state = 1 # reading egobot plans

            if state==0:
                if "(" in line:
                    start = line.split(":")[0]
                    duration = line.split("[")[1][:-2]
                    if line.split(":")[0]=="0.000" and cost!="-":
                        plan_offset = float(cost)
                    c = plan_offset + float(start) + float(duration)
                    if cost=="-" or float(cost) < c:
                        cost = str(c)
            else:
                if "(" in line:
                    start = line.split(":")[0]
                    duration = line.split("[")[1][:-2]
                    c = float(start)+float(duration)
                    if cost=="-" or float(cost) < c:
                        cost = str(c)

        time = line
        print(time+","+cost,end=",")

    # single agent
    cost = "-"
    time = "-"
    with open(dir+"/"+single_agent_file) as saf:
        lines = saf.readlines()
        for line in lines:
            if "; Plan found with metric " in line:
                cost = line[len("; Plan found with metric "):].strip()
            if "; Time " in line:
                time = line[len("; Time "):].strip()
        print(time+","+cost,end="")
    print("")
    
    

