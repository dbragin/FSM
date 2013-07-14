#!/usr/bin/env python

class memory:
    
    def __init__(self):
        self.storage = {}
        self.opMatrix = {'S<': 'append',
                         'S>': 'pop',
                         'L<': '__setitem__',
                         'L>': '__getitem__'}
        

    def operation(self, action, elem = None):
        for op in action.split(","):
            ptr, act = op[:2],op[2:]
            if ptr != "S'":
                try:
                    m = self.storage[ptr]
                except KeyError:
                    self.storage[ptr] = []
                    m = self.storage[ptr]
                operation = m.__getattribute__(self.opMatrix[ptr[:1]+act[:1]])
                if act[1:2] == 'v':
                    value = act[2:]
                cnt = 1
                if act[1] == 'r':
                    cnt = length(elem['link'])
                    for x in range(cnt):
                        operation(act[2:])
                if act[:1] == '<':
                    if value != None:
                        operation(value)
                    else:
                        operation()
                elif act[:1] == '>':
                    if value != None:
                       if value != operation():
                           raise RuntimeError('Not balanced brace:' + value)
                    else:
                        operation()
                

    def debug(self):
        print "Memory storage:"
        for s in self.storage:
            print "-----"
            print s
            print "-----"
            for s1 in self.storage[s]:
                print s1
