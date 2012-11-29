#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

def menu():
	#Create MenuBar
	MenuBar = wx.MenuBar()
	MenuBar.SetBackgroundColour('#d3d3d3')
	
	# Create MenuEntry	
	File = wx.Menu()
	Help = wx.Menu()
        Edit = wx.Menu()

	# Add entry to MenuEntry File
	File.Append(2,'&Add\tctrl+a')
	File.AppendSeparator()
	File.Append( 1, '&Quit\tctrl+q')
	# Add entry to MenuEntry Help
        Help.Append(3, '&About\tf12')
    # Add entry yo MenuEntry Edit
        Edit.Append(4, '&Preferences\tctrl+e')

	MenuBar.Append(File,'&File')
        MenuBar.Append(Edit, '&Edit')
	MenuBar.Append(Help, '&Help')
	
	# Return MenuBar instance
	return MenuBar
