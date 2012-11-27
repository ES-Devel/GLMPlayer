#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

description = """GLMPlayer is an mp3 player, it play's audio with gstreamer plugins. Based on Python programming. Able to play different audio formats. Consumes few resources. I especially thank my dear Alejandra Iveth Morales. 
"""

licence = """GLMPlayer is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

GLMPlayer is distributed in the hope that it will be useful and fun, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with GLMPlayer; 
if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA"""

def OnAbout(self):
	"""Set Info Values"""
	info = wx.AboutDialogInfo()
	info.SetIcon(wx.Icon('icons/esdevel.png', wx.BITMAP_TYPE_PNG))
	info.SetName('GLMPlayer')
	info.SetVersion('0.1')
	info.SetDescription(description)
	info.SetCopyright('(C) 2012 EsDevel team')
	info.SetWebSite('http://es-devel.github.com/GLMPlayer/')
	info.SetLicence(licence)
	info.AddDeveloper('William Parras')
	info.AddDocWriter('EsDevel doc group')
	info.AddArtist('EsDevel design group')
	info.AddTranslator('EsDevel translator group')

	wx.AboutBox(info)	
