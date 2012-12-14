#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create aboutWindow
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

from gi.repository import Gtk
import WindowBase

class aboutWindow(WindowBase.window):
	"""aboutWindow class: based on GlmPlayer class
	creates about dialog"""

	def __init__(self,builder,parent):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
		# Base initial Method
