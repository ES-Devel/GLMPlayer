#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel"""

import wx

class Window(wx.Frame):
	def __init__(self,*args,**kwargs):
		wx.Frame.__init__(self,*args,**kwargs)
	def OnQuit(self, event):
		self.Close()
     
    


