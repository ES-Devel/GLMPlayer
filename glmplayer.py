#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from modules import application, util

'''main app'''
def main():
	application.GLMPlayer = wx.App()
	application.main = util.Window(None)
	application.main.SetTitle("GLMPlayer")
	application.main.SetBackgroundColour( wx.Colour( 0, 0, 0))
	application.main.SetMenuBar(util.extMenuBar(application.APP_EXIT))
	util.Toolbar(application.main)
	application.main.Show()
	application.main.Bind(wx.EVT_MENU,application.main.OnQuit,id=application.APP_EXIT)
	application.GLMPlayer.MainLoop()
if __name__=='__main__':
	main()
	
