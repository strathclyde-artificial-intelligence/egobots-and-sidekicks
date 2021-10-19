# egobotsidekickv2.py
# This file is a work in progress.
# This file aims to achieve the full functionality of egobotsidekick.py, but with a better framework that allows new parsing rules to be added more easily.
# This file will use a class of objects with an object instance for each sidekick, that object will include the parsing rules.

class Agent:
    def __init__(self, name = 'undefined', *listactions):
        self.name = name
        self.actions = []
        for x in listactions:
            obj = self.Action(x)
            self.actions.append(obj)
    
    def get_data(self):
        print('This Agent has ' + str(len(self.actions)) + ' actions, listed below.')
        for i, x in enumerate(self.actions):
            print(self.actions[i].get_data())

    class Action:
        def __init__(self, name = 'undefined'):
            self.name = name #a name
            self.identifiers = 'undefined' #the strings which identify this action is in a plan
            self.parsing = [['undefined','undefined']] #a list of pairs of strings which can be used to isolate any pieces of information which must be recorded
            self.function = 'undefined' #the names of any functions used to add or modify the next problem file based on reading this action in the previous plan
        
        def set_identifiers(self, *identifiers):
            self.identifiers = identifiers
        
        def set_parsing(self, parsing = [['undefined','undefined']]):
            self.parsing = parsing

        def set_function(self, *functionnames):
            self.function = functionnames

        def get_data(self):
            print('Action: ' + self.name)
            print('Identifier: ' + str(self.identifiers))
            print('Parsing Borders: ' + str(self.parsing))
            print('Function Names: ' + str(self.function))

egotosid = Agent('sid','inspect','dropwelder','droppatch','egodropwelder')

egotosid.actions[0].set_identifiers('sid','inspect')
egotosid.actions[0].set_parsing([' pn',' '])
egotosid.actions[0].set_function('addinspectrequest')

egotosid.actions[1].set_identifiers('sid','dropwelder')
egotosid.actions[1].set_parsing([' l',' '])
egotosid.actions[1].set_function('addwelderrequest')

egotosid.actions[2].set_identifiers('sid','droppatch')
egotosid.actions[2].set_parsing([' l',' '])
egotosid.actions[2].set_function('addpatchrequest')

egotosid.actions[3].set_identifiers('ego','dropwelder')
egotosid.actions[3].set_parsing([' l',' '])
egotosid.actions[3].set_function('addegowelderdrop')

#sid.get_data()

sidtoego = [1,2,3,4]
for i, x in enumerate(sidtoego):
    sidtoego[i] = Agent('ego'+str(x),'inspect','dropwelder','droppatch')

    sidtoego[i].actions[0].set_identifiers('sid','inspect')
    sidtoego[i].actions[0].set_parsing([' pn',' '])
    sidtoego[i].actions[0].set_function('modifyinspectgoal')

    sidtoego[i].actions[1].set_identifiers('sid','dropwelder')
    sidtoego[i].actions[1].set_parsing([' l',' '])
    sidtoego[i].actions[1].set_function('addwelderdrop')

    sidtoego[i].actions[2].set_identifiers('sid','droppatch')
    sidtoego[i].actions[2].set_parsing([' l',' '])
    sidtoego[i].actions[2].set_function('addpatchdrop')

#Any time one of these functions is called, it ought to be followed by:
#file = newfile
#additions = additions + newaddition
def addinspectrequest(file, panel, deadline):
    newfile = file
    newaddition = '\n'+'(= (ingoal '+panel+') 1)'+'\n'+'(is-not-inspected '+panel+')'+'\n'+'(at '+deadline+' (not (is-not-inspected '+panel+')))'
    return newfile, newaddition

def addwelderrequest(file, droplocation, deadline):
    newfile = file
    newaddition = '\n'+'(= (wegoal '+droplocation+') 10)'+'\n'+'(welder-drop-needed '+droplocation+')'+'\n'+'(at '+deadline+' (not (welder-drop-needed '+droplocation+')))'
    return newfile, newaddition

def addpatchrequest(file, location, deadline):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def addegowelderdrop(file, location, time):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def modifyinspectgoal(file, panels): # this function takes in a list of all the panels, if you do only one panel at a time it will be slower
    sep1 = file.partition(';goalstart') # this comment must be located at the start of the egobot's goals
    sep2 = sep1.partition(';goalend') # this comment must be located at the end of the egobot's goals
    sep3 = sep2.splitlines()
    newgoals = ''
    for line in sep3:
        for panel in panels:
            if panel in line:
                newgoals = newgoals + '\n'+';'+line
            else:
                newgoals = newgoals + '\n'+line
    newfile = sep1[0]+sep1[1]+newgoals+'\n'+sep2[1]+sep2[2]
    newaddition = ''
    return newfile, newaddition

def addwelderdrop(file):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def addpatchdrop(file):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def outputparser(file): # this function extracts a plan from a planner's output log
    splitbyplan = file.split('[0.000]:')
    lastplan = splitbyplan[-1]
    lastplanlines = lastplan.splitlines()
    plan = ''
    for line in lastplanlines:
        if ': (' in line:
            plan = plan + '\n' + line
    return plan

def planparser(plan, action): # this function parses a plan string for information contained in the parsing pairs on lines identified by identifiers
    planlines = plan.splitline()
    identifiers = action.identifiers
    parsing = action.parsing
    relevantlines = []
    keyinfo = []
    keyinfo[0] = []
    for line in planlines():
        if all(key in line for key in identifiers): # the line must contain every identifier string to be accepted
            relevantlines.append(line)
    for line in relevantlines:
        for i, pair in enumerate(parsing): # parsing is a list of lists of strings, each list of strings has two strings
            sep1 = line.partition(pair[0]) # cut off the part of the line before the info to be parsed
            sep2 = sep1[2].partition(pair[1]) # cut off the part of the line after the info to be parsed
            keydatum = sep1[1]+sep2[0]+sep2[1] # combine the parsing strings with the contained string
            keyinfo[i].append(keydatum.strip()) # the spaces used in the parsing strings are removed by the .strip()
    lastrelevantline = relevantlines[-1]
    timesep1 = lastrelevantline.partition(':') # extract starting time of the last line
    timesep2a = timesep1.partition(' [') # extract duration of the first time
    timesep2b = timesep2a.partition(']') # trim square bracket off the duration
    lastlinestart = timesep1[0]
    lastlinedur = timesep2b[0]
    deadline = str(float(lastlinestart)+float(lastlinedur))
    return keyinfo, deadline # a list of lists of strings such as panels and a string giving the end time of the last request
            