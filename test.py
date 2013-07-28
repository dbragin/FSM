#!/usr/bin/env python
# -*- coding: utf-8 -*-

import FSMLoader

import xmlParser


fin = open("sample/input_test.txt")

diagramm = xmlParser.XmlUtil.readXml(fin.read())

diagramm.startWith('A0')

loader = FSMLoader.FSMLoader()
fsm = loader.load("Activity")

errors = diagramm.check(fsm)
print errors

#fsm.debug()



