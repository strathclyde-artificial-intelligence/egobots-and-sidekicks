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

def addwelderrequest(file, location, deadline):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def addpatchrequest(file, location, deadline):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def addegowelderdrop(file, location, time):
    newfile = file
    newaddition = ''
    return newfile, newaddition

def modifyinspectgoal(file):
    newfile = file
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