#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

def ToolBar(parent):
    ToolBar = wx.ToolBar(parent)
    ToolBar.SetToolBitmapSize(wx.Size(25,25))
    return ToolBar