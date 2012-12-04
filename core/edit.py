#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create editWindow
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

import gtk 
import window

class editWindow(window.Glmplayer):
	def __init__(self,builder,parent):
		window.Glmplayer.__init__(self,parent)
		self.__instance = None	
		self.__builder = builder
	
	def Start(self):
		self.__instance =  self.__builder.get_object("edit")

	def Set(self):
		pass
	
	def edicion(self,widget):
		"""edit meta data"""
		try:
			select = self.__parent.tree.get_selection()
			filepath = path.on_tree_selection_changed(select)
			tag = eyeD3.Tag()
			tag.link(filepath)
			self.getParent().stock_album.set_text(tag.getAlbum())
			self.getParent().stock_interp.set_text(tag.getArtist())
			self.getParent().stock_titulo.set_text(tag.getTitle())
			self.__instance.show()
		except:
			pass

	def stop_edicion(self,widget):
		"""hide editor"""
		self.__instance.hide()

	def save(self,widget):
		"""save changes to meta data"""
		select = self.__parent.tree.get_selection()
		filepath = path.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		tag.link(filepath)
		tag.setAlbum(self.getParent().stock_album.get_text())
		tag.setArtist(self.getParent().stock_interp.get_text())
		tag.setTitle(self.getParent().stock_titulo.get_text())
		tag.update()
		self.__instance.hide()

	
