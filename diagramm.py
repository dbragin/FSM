class Diagramm:
    
    def __init__(self):
        self.elements = {}
        self.startId = None
        self.linkStack = []
        self.errors = []
        
    def addElement(self, type, uid):
        self.elements[uid] = {}
        self.elements[uid]['type'] = type
        self.elements[uid]['uid'] = uid
		
    def addLink(self, uid, uidSource, uidTarget):
        try:
            self.elements[uidSource]['link'].append({'uid':uid, 'target':uidTarget})
	except KeyError:
            self.elements[uidSource]['link'] = []
            self.elements[uidSource]['link'].append({'uid':uid, 'target':uidTarget})
            
    def startWith(self, typeName):
        for k,v in self.elements.items():
            if v['type'] == 'A0':
                self.startId = k

    def __str__(self):
        return 'Start with ' + self.startId.__str__() + '\n' + self.elements.__str__()

    def check(self, fsm):
	tmpDiagram = self.elements.copy()
        elem = tmpDiagram[self.startId]
	
	self.linkStack.append(elem['link'][0])
	fsm.execute(elem['type'], elem)
      
        process = True
        while process:
            try:
                label = self.linkStack.pop()
                fsm.execute('label')
		elem = tmpDiagram[label['target']]
                a = fsm.execute(elem['type'], elem)
                if a[:2] == "S'":
                    tmp = None
                    for c in a[2:]:
                        if c == '>':
                            tmp = self.linkStack.pop()
                    for l in elem['link']:
                        self.linkStack.append(l)
                    if tmp != None :
                        self.linkStack.append(tmp)
            except IndexError:
                print elem
                self.errors.append({'text':"No links",'id':elem['uid']})
                process = False
                pass
            except Exception,e:
                if elem['type'] == 'Ak':
                    process = False
                    pass
                else:
                    print self.linkStack
                    print "Error", e
		    error = 'Link is missing'
                    if (e.__str__() == "Not balanced brace"):
			error = e.__str__()
                    self.errors.append({'text': error,'id': elem['uid']})
                    process = False
                    pass
        return self.errors

