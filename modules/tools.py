#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Copyright (c) 2012 - EsDevel team
   License: GPL"""

import wx

class generator:
	"""class provide functions to generate toolbar quickly"""
	def uiMenuBtn(self,ext,path,btn):
		"""return JSON object, content: dic"""
		_buffer = {}
		i = 1
		if str(type(btn)).find('tuple') >= 0:
			for j in btn:
				if j == 1:
					_buffer['separator'+str(i)] = 1
					i = i + 1
				else:
					_buffer[j]=path+str(j)+ext
		else:
			pass 
		return _buffer

	def getReference(self,toolbar,imgPath,items,btn_dic):
		"""Reference to menu objects"""
		ref = {}
		ref['play'] = toolbar.AddTool(wx.ID_ANY,wx.Bitmap(imgPath+'play.png'),\
		wx.Bitmap(imgPath+'play.png'),True)
		for button in items:
			if button == 1:
				ref['separator'+str(button)] = toolbar.AddSeparator()
			else: 
				ref[button] = toolbar.AddLabelTool(wx.ID_ANY,button,\
				wx.Bitmap(btn_dic[button]))				
		return ref

	def SetBold(self,repLabel):
		"""set text to Bold"""
		Bold = repLabel.GetFont()
		Bold.SetWeight(wx.BOLD)
		repLabel.SetFont(Bold)

	def AddGenericControl(self,toolbar,*args):
		"""Add new generic control"""
		for control in args:
			toolbar.AddControl(control)
		toolbar.Realize()

	def Thumb(self,img):
		icon = wx.Image(img, wx.BITMAP_TYPE_ANY)
		icon = icon.Scale(50,50,100)
		return icon.ConvertToBitmap()

	def MediaHeaders(self,List,*args):
		i = 0
		for head in args:
			List.InsertColumn(i, head[0], width=head[1])
