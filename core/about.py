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
	"""aboutWindow class: based on GlmPlayer class
	creates about dialog"""

	def __init__(self,builder,parent):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		window.Glmplayer.__init__(self,parent,builder)
		# Base initial Method
	
	def Start(self,name):
		"""Start method: build window (overload)
		:param name: window name to be created
		:return: None"""
		self.instance(self.getBuilder().get_object(name))

	def Set(self):
		"""Set Method: (overload)
		:return: None"""
		pass
	
	
