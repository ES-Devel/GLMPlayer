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

class Glmplayer(object):
	"""Glmplayer class: window base"""

	def __init__(self,parent,builder):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		self.__parent = parent
		self.__instance = None
		self.__builder = builder

	def Set(self):
		"""Set Method: set builder
		:return: None"""
		self.__builder = gtk.Builder()
		self.__builder.add_from_file(resources.ui())


	def Start(self,name):
		"""Start method: build window
		:param name: window name to be created
		:return: None"""
		self.instance(self.getBuilder().get_object(name))
		# get gtk.Widow Instance, then get window objects
		self.__parent.tree = self.__builder.get_object("arbol_pistas")
        	self.__parent.medialist = self.__builder.get_object("media")
        	self.__parent.sel = self.__builder.get_object("selec")
        	self.__parent.imagen = self.__builder.get_object("caratula")
        	self.__parent.info = self.__builder.get_object("info")
        	self.__parent.artista = self.__builder.get_object("artista")
        	self.__parent.album = self.__builder.get_object("album")
        	self.__parent.titulo = self.__builder.get_object("titulo")
        	self.__parent.duracion = self.__builder.get_object("duracion")
        	self.__parent.volumen = self.__builder.get_object("volumen")
        	self.__parent.progressBar = self.__builder.get_object("bar")
        	self.__parent.stock_interp = self.__builder.get_object("stock_interp")
       		self.__parent.stock_titulo = self.__builder.get_object("stock_titulo")
        	self.__parent.stock_album = self.__builder.get_object("stock_album")

	def getBuilder(self):
		"""getBuilder method: get window builder
		:return: gtk.Builder"""
		return self.__builder

	def getParent(self):
		"""getParent method: get parent class
		:return: extended object class"""
		return self.__parent

	def getInstance(self):
		"""getInstance method: get window instance
		:return: gtk.Window"""
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
