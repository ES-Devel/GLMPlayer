#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create window instance
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

import gtk
import resources
import WindowBase

class Glmplayer(WindowBase.window):
	"""Glmplayer class: window base"""

	def __init__(self,parent,builder):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
		
	def Start(self,name,objects):
		"""Start method: build window
		:param name: window name to be created
		:param objects: type -> tuple, objects in window
		:return: None"""
		self.instance(self.getBuilder().get_object(name))
		# get gtk.Widow Instance, then get window objects
		self.getParent().child = { }
		for item in objects:
			self.getParent().child[item] = self.getBuilder().get_object(item)

