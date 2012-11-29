#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""copyright (c) 2012 - EsDevel"""

import wx
from core import menu
from core import toolBar
from extra import binding 
from core import mediaList

def startBuilding(window):
    window.SetMenuBar(menu.menu( )) 
    window.SetToolBar(toolBar.ToolBar(window))
    binding.Events(window)
    window.CreateStatusBar()
    panel = wx.Panel(window)
    leftPanel = wx.Panel(panel)
    rigthPanel = wx.Panel(panel)
    panel.SetBackgroundColour('#4f5049')
    leftPanel.SetBackgroundColour('#000000')
    rigthPanel.SetBackgroundColour('#ffffff')
    hBoxMain = wx.BoxSizer(wx.HORIZONTAL)
    rightBox = wx.BoxSizer(wx.VERTICAL)
    
    list = mediaList.AutoWidthListCtrl(rigthPanel)
    MediaHeaders(list,('Artist',140),('Album',140),('Duration',140))
    
    hBoxMain.Add(leftPanel, 1, flag = wx.EXPAND|wx.RIGHT|wx.LEFT, border = 20)
    hBoxMain.Add(rigthPanel, 2, wx.EXPAND)
    rightBox.Add(list, 1, wx.EXPAND)
    panel.SetSizer(hBoxMain)
    rigthPanel.SetSizer(rightBox)
    
def MediaHeaders(List,*args):
    i = 0
    for head in args:
        List.InsertColumn(i, head[0], width=head[1])
