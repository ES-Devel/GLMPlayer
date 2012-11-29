#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel team"""

import wx 
import os

wildcard = "mp3 files (*.mp3)|*.mp3|"
message = "Import audio files"
defaultDir = os.getcwd()
defaultFile=""
style = wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR

class AddDialog(wx.FileDialog):
	def __init__(self, parent):
		wx.FileDialog.__init__(self, parent, message, defaultDir,\
		defaultFile, wildcard, style)
        
def LaunchFileDialog(ev):
    dialog = AddDialog(None)                      
    if dialog.ShowModal() == wx.ID_OK:
        paths = dialog.GetPaths()
        for path in paths:
            print path
    dialog.Destroy( )
