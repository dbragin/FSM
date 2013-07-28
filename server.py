#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import os
import random

import FSMLoader
import xmlParser

from xml.etree import ElementTree 

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hellow world!")
	def post(self):
		self.set_header("Content-Type","application/xml")
		s = self.request.body
		typematrix = {"UML_ActivityStartModel":lambda:"A0",
                      "UML_ActivityEndModel":lambda:"Ak",
                      "UML_ActivityActionModel":lambda:"A",
                      "UML_ActivityBranchStartModel":lambda:"P",
                      "UML_ActivityBranchEndModel":lambda:"W",
                      "UML_ActivityForkStartModel":lambda:"R",
                      "UML_ActivityForkEndModel":lambda:"L"
                      }

		d = xmlParser.XmlUtil.readXml(s,typematrix)
                d.startWith('A0')
                loader = FSMLoader.FSMLoader()
                fsm = loader.load("Activity")

                er = d.check(fsm)
                fsm.debug()
		
		self.write(xmlParser.XmlUtil.dictToXml(er))

class TestHandler(tornado.web.RequestHandler):
	
	def get(self):
		self.write("Use only POST request")

	def post(self):
		self.set_header("Content-Type", "application/xml")
		typematrix = {"Initial State":lambda:"A0",
                      "Final State":lambda:"Ak",
                      "State":lambda:"A",
                      "Decision":lambda:"P",
                      "Decision End":lambda:"W",
                      "Transition (Fork)":lambda:"R",
                      "Transition (Join)":lambda:"L"
                      }
		diagramm = xmlParser.XmlUtil.readXml(self.request.body, typematrix)
		diagramm.startWith('A0')

		loader = FSMLoader.FSMLoader()
		fsm = loader.load("Activity")

		errors = diagramm.check(fsm)
		xmlResponse = xmlParser.XmlUtil.dictToXml(errors)
		print xmlResponse
		self.write(xmlResponse)

application = tornado.web.Application([
	(r"/uml", MainHandler),
	(r"/test", TestHandler),
])

if __name__ == "__main__":
	print "Server start at port 8888"
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
