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
import WindowBase
import resources
import eyeD3

class editWindow(WindowBase.window):
	"""editWindow class: based on GlmPlayer class
	creates edit dialog"""

	def __init__(self,builder,parent):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
	
	def edicion(self,widget):
		"""edicion method: edit metadata
		:return: None"""
		try:
			select = self.getParent().tree.get_selection()
			filepath = resources.on_tree_selection_changed(select)
			tag = eyeD3.Tag()
			tag.link(filepath)
			self.getParent().stock_album.set_text(tag.getAlbum())
			self.getParent().stock_interp.set_text(tag.getArtist())
			self.getParent().stock_titulo.set_text(tag.getTitle())
			self.Show_()
		except:
			pass

	def stop_edicion(self,widget):
		"""stop_edicion method: hide editor
		:return: None"""
		self.Hide_()

	def save(self,widget):
		"""save method: save changes to meta data
		:return: None"""
		select = self.getParent().tree.get_selection()
		filepath = resources.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		tag.link(filepath)
		tag.setAlbum(self.getParent().stock_album.get_text())
		tag.setArtist(self.getParent().stock_interp.get_text())
		tag.setTitle(self.getParent().stock_titulo.get_text())
		tag.update()
		self.Hide_()
