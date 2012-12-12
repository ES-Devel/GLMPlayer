#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Window Base
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

from gi.repository import Gtk, GObject
import resources

class window(object):
	"""Glmplayer class: window base"""

	def __init__(self,parent,builder):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: Gtk.Builder
		:return: None"""
		self.__parent = parent
		self.__instance = None
		self.__builder = builder

	def Start(self,name):
		"""Start method: build window
		:param name: window name to be created
		:return: None"""
		self.instance(self.getBuilder().get_object(name))

	def getBuilder(self):
		"""getBuilder method: get window builder
		:return: Gtk.Builder"""
		return self.__builder

	def getParent(self):
		"""getParent method: get parent class
		:return: extended object class"""
		return self.__parent

	def getInstance(self):
		"""getInstance method: get window instance
		:return: Gtk.Window"""
		return self.__instance

	def Show(self,widget):
		"""Show method: event method
		:return: None"""
		self.getInstance().show()

	def Show_(self):
		"""Show_ method: the same as Show,
		but this is called manually
		:return: None"""
		self.getInstance().show()
	
	def Hide(self,widget):
		"""Hide method: event method
		:return: None"""
		self.getInstance().hide()

	def Hide_(self):
		"""Hide_ method: the same as Hide,
		but this is called manually
		:return: None"""
		self.getInstance().hide()
	
	def instance(self,instance):
		"""instance method: set instance
		:return: None"""
		self.__instance = instance 
