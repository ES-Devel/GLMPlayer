#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from window import about
from window import openFiles

def Events(window):
	window.Bind(wx.EVT_MENU,window.OnQuit,id=1)
	window.Bind(wx.EVT_MENU,about.OnAbout, id=3)
	window.Bind(wx.EVT_MENU,openFiles.LaunchFileDialog, id=2)