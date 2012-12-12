#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create editWindow
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

from gi.repository import Gtk, GObject
import WindowBase
import resources
import eyeD3

class editWindow(WindowBase.window):
	"""editWindow class: based on GlmPlayer class
	creates edit dialog"""

	def __init__(self,builder,parent,MediaTree):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: Gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
		self.Tree = MediaTree
	
	def edicion(self,widget):
		"""edicion method: edit metadata
		:return: None"""
		try:
			select = self.Tree.get_selection()
			filepath = resources.on_tree_selection_changed(select)
			tag = eyeD3.Tag()
			tag.link(filepath)
			self.getParent().child["stock_album"].set_text(tag.getAlbum())
			self.getParent().child["stock_interp"].set_text(tag.getArtist())
			self.getParent().child["stock_titulo"].set_text(tag.getTitle())
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
		select = self.Tree.get_selection()
		filepath = resources.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		tag.link(filepath)
		tag.setAlbum(self.getParent().child["stock_album"].get_text())
		tag.setArtist(self.getParent().child["stock_interp"].get_text())
		tag.setTitle(self.getParent().child["stock_titulo"].get_text())
		tag.update()
		self.Hide_()
