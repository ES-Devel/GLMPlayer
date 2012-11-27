#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel team
   License: GPL"""

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class repControl(wx.Slider):
	"""create slider for volume"""
	def __init__(self,parent):
		wx.Slider.__init__(self,parent, 5, 6, 1, 10, (120, 90), (110, -1))

class AutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
	"""Auto Width List for media"""
	def __init__(self, parent):
        	wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        	ListCtrlAutoWidthMixin.__init__(self)
