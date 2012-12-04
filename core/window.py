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
	"""main window"""

	def __init__(self,parent):
		"""init method
		:return: None
		"""
		self.__parent = parent

	def Set(self):
		self.__builder = gtk.Builder()
		self.__builder.add_from_file(resources.ui())

	def Start(self):
		"""conect window child
		:return: None
		:param parent: main obj"""
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
		""":return gtk.Builder:"""
		return self.__builder

	def getParent(self):
		return self.__parent
