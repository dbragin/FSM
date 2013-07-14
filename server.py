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
		p = Popen(['AnalizerUtil'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
		self.set_header("Content-Type","application/xml")
		self.write(p.stdout.read())

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


class SandboxHandler(tornado.web.RequestHandler):

	def get(self):
		self.write("Use only POST request")

	def post(self):
		self.set_header("Content-Type","application/xml")
		s = self.request.body
		probability = float(self.get_argument("probability",0.3))
		d = xmlParser.XmlUtil.readXml(s)
		errors = []
		for el in d.elements:
			if random.random() < probability : 
				errors.append({'text': d.elements[el]['type'],'id':el})
			#for l in d.elements[el]['link']
		self.write(xmlParser.XmlUtil.dictToXml(errors))

application = tornado.web.Application([
	(r"/uml", MainHandler),
	(r"/sandbox", SandboxHandler),
])

if __name__ == "__main__":
	print "Server start at port 8888"
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
