#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Copyright (c) 2012 - EsDevel team
   License: GPL"""

import wx
import tools
import controls
import sys

ToolsGenerator = tools.generator()
"""Tool object"""

imgPath = 'icons/' 
"""Easy way to change icons directory"""

class Window(wx.Frame):
	"""return window instance"""
	def __init__(self,parent,*args,**kwargs):
		super(Window,self).__init__(parent,*args,**kwargs)
		
  		# Boxes
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		vbox = wx.BoxSizer(wx.VERTICAL)
		hbox2 = wx.BoxSizer(wx.HORIZONTAL)

		# Panel
		self.panel = wx.Panel(self, -1)
		
		# PlayBar indic
		self.rep = controls.repControl(self.panel)
		
		# MediaList
		self.list = controls.AutoWidthListCtrl(self.panel)
		ToolsGenerator.MediaHeaders(self.list,('Artist',140),\
		('Album',140),('Duration',140))	
		
		# StatusBar	
		self.CreateStatusBar()
	
		# Setting position for items in window
		hbox.Add(self.list, 1, wx.EXPAND,border=0)
		hbox2.Add(self.rep,1,border=0)
		vbox.Add(hbox2,1, wx.EXPAND,border=0)
		vbox.Add(hbox,1, wx.EXPAND,border=0)
        	self.panel.SetSizer(vbox)
		self.Centre()

	def OnQuit(self, event):
		self.Close()

def extMenuBar(APP_EXIT):
	"""return menu instance"""

	#Create MenuBar
	MenuBar = wx.MenuBar()
	MenuBar.SetBackgroundColour('#d3d3d3')
	
	# Create MenuEntry	
	File = wx.Menu()
	Help = wx.Menu()
	
	# Add entry to MenuEntry File
	Quit = wx.MenuItem(File, APP_EXIT, '&Quit\tctrl+q')
	File.Append(wx.ID_NEW,'&Add\tctrl+a')
	File.AppendSeparator()
	File.AppendItem(Quit)
	
	# Add entry to MenuEntry Help
        Help.Append(200, '&About')
	
	# Add menuEntry to MenuBar
	MenuBar.Append(File,'&File')
	MenuBar.Append(Help, '&Help')
	
	# Return MenuBar instance
	return MenuBar 

def Toolbar(window):
	"""add TooBar on target window"""
	
	items = ('cancel','right','left',1,'tweet','about','add','delete',1) 
	btn_dic= ToolsGenerator.uiMenuBtn('.png',imgPath,items)

	toolbar = window.CreateToolBar()

	ref = {}
	ref = ToolsGenerator.getReference(toolbar,imgPath,items,btn_dic)
	"""Get reference for objects on toolbar"""

        artwork = ToolsGenerator.Thumb(imgPath+'cd.png')
 
        artwork_btn = wx.BitmapButton(toolbar, id=-1, bitmap=artwork,pos=(10, 20),\
	size = (artwork.GetWidth()+10, artwork.GetHeight()+10))
	
	repLabel = wx.StaticText(toolbar,id=-1,label="   No se reproduce nada",size=wx.Size(200,10))
	ToolsGenerator.SetBold(repLabel)
	ToolsGenerator.AddGenericControl(toolbar,artwork_btn,repLabel)

	

