#!/usr/bin/env python

class memory:
    
    def __init__(self):
        self.storage = {}
        self.opMatrix = {'S<': 'append',
                         'S>': 'pop',
                         'L<': '__setitem__',
                         'L>': '__getitem__'}
        

    def operation(self, action, elem = None):
        
	for operations in action.split(","):
            ptr, act = operations[:2], operations[2:]
	    
	    print "Operation ", operations 
	    print "Ptr: ", ptr, " Act:", act
            
	    if ptr != "S'":
                try:
                    m = self.storage[ptr]
                except KeyError:
                    self.storage[ptr] = []
                    m = self.storage[ptr]

                operation = m.__getattribute__( self.opMatrix[ ptr[:1] + act[:1] ] )
		print "operation: ", operation
                
		if act[1:2] == 'v':
		    print "v", act[2:]
                    value = act[2:]

                if act[1] == 'r':
                    cnt = len(elem['link'])
		    value = act[2:]
		    print "r", act[2:], cnt
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
                           raise RuntimeError('Not balanced brace')
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
