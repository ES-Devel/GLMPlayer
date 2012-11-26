#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Copyright (c) 2012 - EsDevel team
   Distributed under GLP License"""

import wx

"""Shortcut icons"""
def shorcut():
	return 'icons/'

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
"""create img Path's for each button"""
imgPath = shorcut()
lb = ('Play','Stop','Next','Prev','Paus')
img = {lb[0]:'play.png',lb[1]:'cancel.png',lb[2]:'right.png',lb[3]:'left.png',lb[4]:'pause.png'}
lb2 = ('Tweet','About','Add','Delete')
img2 = {lb2[0]:'tweet.png',lb2[1]:'about.png',lb2[2]:'add.png',lb2[3]:'delete.png'}
"""create ToolBar"""
def Toolbar(window):
	"""ToolBar instance"""
	toolbar = window.CreateToolBar()
	"""Play controller"""
	btns = []
	"""tools on ToolBar"""
	tools = []
	"""Reference for each button in order"""
	ref = {}
	for i in range(0,4):
		btns.append((lb[i],imgPath+img[lb[i]]))
	for i in range(0,3):
		tools.append((lb2[i],imgPath+img2[lb2[i]]))
	for bt in btns:
		btn = toolbar.AddLabelTool(wx.ID_ANY,bt[0],wx.Bitmap(bt[1]))
		ref[bt[0]]= btn
	sep = toolbar.AddSeparator()
	for bt in tools:
		btn = toolbar.AddLabelTool(wx.ID_ANY,bt[0],wx.Bitmap(bt[1]))
		ref[bt[0]]= btn
	delete_btn = toolbar.AddLabelTool(wx.ID_ANY,"Delete",wx.Bitmap(imgPath+"delete.png"))
	toolbar.Realize()
	
