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
		
	def Start(self,name):
		"""Start method: build window
		:param name: window name to be created
		:return: None"""
		self.instance(self.getBuilder().get_object(name))
		# get gtk.Widow Instance, then get window objects
		self.getParent().tree = self.getBuilder().get_object("arbol_pistas")
		self.getParent().medialist = self.getBuilder().get_object("media")
		self.getParent().sel = self.getBuilder().get_object("selec")
		self.getParent().imagen = self.getBuilder().get_object("caratula")
		self.getParent().info = self.getBuilder().get_object("info")
		self.getParent().artista = self.getBuilder().get_object("artista")
		self.getParent().album = self.getBuilder().get_object("album")
		self.getParent().titulo = self.getBuilder().get_object("titulo")
		self.getParent().duracion = self.getBuilder().get_object("duracion")
		self.getParent().volumen = self.getBuilder().get_object("volumen")
		self.getParent().progressBar = self.getBuilder().get_object("bar")
		self.getParent().stock_interp = self.getBuilder().get_object("stock_interp")
		self.getParent().stock_titulo = self.getBuilder().get_object("stock_titulo")
		self.getParent().stock_album = self.getBuilder().get_object("stock_album")

