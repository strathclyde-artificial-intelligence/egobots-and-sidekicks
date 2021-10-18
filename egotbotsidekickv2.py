# egobotsidekickv2.py
# This file is a work in progress.
# This file aims to achieve the full functionality of egobotsidekick.py, but with a better framework that allows new parsing rules to be added more easily.
# This file will use a class of objects with an object instance for each sidekick, that object will include the parsing rules.

class Sidekick:
    def __init__(self, identifier, *listactions):
        self.identifier = identifier #the string which refers to this agent in PDDL
        self.actions = []
        for x in listactions:
            obj = self.Action(x)
            self.actions.append(obj)
    
    def get_data(self):
        print('This Sidekick has ' + str(len(self.actions)) + ' actions, listed below.')
        for i, x in enumerate(self.actions):
            print(self.actions[i].get_data())

    class Action:
        def __init__(self, name = 'undefined', identifier = 'undefined', parsing = [['undefined','undefined']], addline = 'undefined', modifyline = 'undefined'):
            self.name = name #a name
            self.identifier = identifier #the string which will only appear in a Sidekick's Action (in the Egobot's plan) when this Action is being taken
            self.parsing = parsing #a list of pairs of strings which can be used to isolate any pieces of information which must be recorded
            self.addline = addline #the name of a function that creates a line to be added based on this action
            self.modifyline = modifyline #the name of a function that parses for and modifies lines based on this action
        
        def get_data(self):
            print('Action: ' + self.name)
            print('Identifier: ' + self.identifier)
            print('Parsing Borders: ' + str(self.parsing))
            print('Add Line Function: ' + self.addline)
            print('Modify Line Function: ' + self.modifyline)

sid = Sidekick('inspect','dropwelder','droppatch')
sid.actions[0].identifier = 'inspect'
sid.actions[0].parsing = ['pn',' ']
sid.actions[0].addline = 'addinspectline()'
sid.get_data()
#gavin = sid.actions[0]
#gavin = Action(gavin)
#sid.create_actions()