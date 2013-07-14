#!/usr/bin/env python

import memory

class FSM:
    def __init__(self):
        self.states = {}
        self.state = None
        self.memory = memory.memory()

    def start(self, state):
        self.state = state

    def add(self, state, signal, new_state, action = ""):
        try:
            self.states[state][signal] = (new_state, action)
        except KeyError:
            self.states[state] = {}
            self.states[state][signal] = (new_state, action)
    
    def execute(self, signal, elem = None):
        if self.state not in self.states:
            raise RuntimeError("No state")
        state = self.states[self.state]
        if signal in state:
            new_state, action = state[signal]
            self.memory.operation(action,elem)
            self.state = new_state
            return action.split(',')[0]
        else:
            raise RuntimeWarning("No edge")
            
    def debug(self,onlyMemory = False):
        if not onlyMemory:
            for state in self.states:
                print state
            print self.state
        self.memory.debug()
            
        
        
