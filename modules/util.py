#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Copyright (c) 2012 - EsDevel team
   Distributed under GLP License"""

import wx
"""Get window instance"""
class Window(wx.Frame):
	def __init__(self,parent,*args,**kwargs):
		super(Window,self).__init__(parent,*args,**kwargs)
	def OnQuit(self, event):
		self.Close()
"""create MenuBar """
def extMenuBar(APP_EXIT):
	MenuBar = wx.MenuBar()
	MenuBar.SetBackgroundColour('#d3d3d3')
	fileMenu = wx.Menu()
	Quit = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tctrl+q')
	fileMenu.Append(wx.ID_NEW,'&Add\tctrl+a')
	fileMenu.AppendSeparator()
	fileMenu.AppendItem(Quit)
	MenuBar.Append(fileMenu,'&File')
	return MenuBar
"""create ToolBar"""
def Toolbar(window):
	toolbar = window.CreateToolBar()
	btns = []
	ref = {}
	btns.append(('Play','icons/play.png'))
	btns.append(('Stop','icons/cancel.png'))
	btns.append(('Next','icons/right.png'))
	btns.append(('Prev','icons/left.png'))
	btns.append(('Paus','icons/pause.png'))
	for bt in btns:
		btn = toolbar.AddLabelTool(wx.ID_ANY,bt[0],wx.Bitmap(bt[1]))
		ref[bt[0]]= btn
	sep = toolbar.AddSeparator()
	toolbar.Realize()
	
