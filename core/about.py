#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create aboutWindow
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

import gtk 
import window

class aboutWindow(window.Glmplayer):
	def __init__(self,builder,parent):
		window.Glmplayer.__init__(self,parent)
		self.__instance = None	
		self.__builder = builder
	
	def Start(self):
		self.__instance =  self.__builder.get_object("about")

	def Set(self):
		pass
	
	def Show(self,widget):
		"""show about window"""
		self.__instance.show()
	
	def Hide(self,widget):
		"""hide about window"""
		self.__instance.hide()
	
