#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Copyright (c) 2012 - EsDevel team
   main application, runs window
   contact to: william.parras.mendez@gmail.com
   Distributed under GLP License"""

import wx
from modules import *

__package__="glmplayer-0.1"

"""main app throws main Loop"""
def main():
	application.GLMPlayer = wx.App()
	application.main = util.Window(None)
	application.main.SetTitle("GLMPlayer")
	application.main.SetMenuBar(util.extMenuBar(application.APP_EXIT))
	util.Toolbar(application.main)
	application.main.Show()
	application.main.Bind(wx.EVT_MENU,application.main.OnQuit,id=application.APP_EXIT)
	application.GLMPlayer.MainLoop()
if __name__=='__main__':
	main()
	
