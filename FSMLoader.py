#!/usr/bin/env python

import json
import fsm

class FSMLoader:
       
    def load(self, name):
        f = open("./gramar/" + name + ".json")
        grammar = json.loads(f.read())
        g = fsm.FSM()
        for rule in grammar:
            g.add(rule.get("state"),rule.get("signal"),rule.get("new_state"),rule.get("action"))
        g.start("INIT")
        return g

