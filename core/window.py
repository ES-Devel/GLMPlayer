#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create window instance
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

from gi.repository import Gtk, GObject
import resources
import WindowBase

class Glmplayer(WindowBase.window):
	"""Glmplayer class: window base"""

	def __init__(self,parent,builder):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: Gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
		
	def Start(self,name,objects):
		"""Start method: build window
		:param name: window name to be created
		:param objects: type -> tuple, objects in window
		:return: None"""
		self.instance(self.getBuilder().get_object(name))
		# get Gtk.Widow Instance, then get window objects
		child = { }
		for item in objects:
			child[item] = self.getBuilder().get_object(item)
		context = child["herramientas"].get_style_context()
		context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
		return child
		

