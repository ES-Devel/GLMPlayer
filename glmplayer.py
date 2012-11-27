#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel team
   License: GPL"""

import wx
from modules import application
from modules import util
from modules import about

__package__="glmplayer-0.1"
"""Version"""

def main():
	"""Main application"""
	# Create main app
	application.GLMPlayer = wx.App()
	# Run main Window 
	application.main = util.Window(None)
	application.main.SetTitle("GLMPlayer")
	# Create Menu
	application.main.SetMenuBar(util.extMenuBar(application.APP_EXIT))
	# Create ToolBar
	util.Toolbar(application.main)
	# Show Window
	application.main.Show()

	# Events
	application.main.Bind(wx.EVT_MENU,application.main.OnQuit,id=application.APP_EXIT)
        application.main.Bind(wx.EVT_MENU, about.OnAbout, id=200)

	# Run Loop - wait for events
	application.GLMPlayer.MainLoop()

if __name__=='__main__':
	"""Run"""
	main()
	
