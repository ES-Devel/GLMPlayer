#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create importWindow
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

import gtk 
import window
from xml.dom.minidom import Document
from xml.dom import minidom
import resources
import os

filepattern = (("MP3","*.mp3"),) 
"""Sopported formats"""

class importWindow(window.Glmplayer):

	def __init__(self,builder,parent):
		window.Glmplayer.__init__(self,parent)
		self.__builder = builder
		self.__instance = None	
		self.filtro = gtk.FileFilter()

	def Start(self):
		self.__instance = self.__builder.get_object("Add")

	def Set(self):
		pass
	
	def OpenDialog(self,widget):
		"""Add files to playlist"""
		pattern = (".mp3") 	
		self.filtro.set_name("*.mp3")
		for name, pattern in filepattern:
 			self.filtro.add_pattern(pattern)         	
		self.__instance.add_filter(self.filtro)
		respt=self.__instance.run()
		self.__instance.remove_filter(self.filtro)
		self.__instance.hide()
		dom = minidom.parse(resources.ConfigFiles()+"track.xml")
		wml = dom.getElementsByTagName('wml')
		if respt == -5:
			fileselected = self.__instance.get_filenames()
			for files in fileselected:
				(dirs,files)= os.path.split(files)
				self.getParent().medialist.append([files,dirs])
				maincard = dom.createElement("pista")
				wml[0].appendChild(maincard)
				nm = dom.createElement("track")
				maincard.appendChild(nm)
				nombre = dom.createTextNode(files)
				nm.appendChild(nombre)
				dr = dom.createElement("ruta")
				maincard.appendChild(dr)
				paths = dom.createTextNode(dirs)
				dr.appendChild(paths)
			xmldocument = open(resources.ConfigFiles()+"track.xml","w")
			dom.writexml(xmldocument)
			xmldocument.close()

	
