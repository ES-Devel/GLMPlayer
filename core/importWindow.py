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
import WindowBase
from xml.dom.minidom import Document
from xml.dom import minidom
import resources
import os

filepattern = (("MP3","*.mp3"),) 
"""Sopported formats"""

class importWindow(WindowBase.window):
	"""importWindow class: based on GlmPlayer class
	creates an openDialog window"""

	def __init__(self,builder,parent,File):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
		# Base initial Method	
		self.filtro = gtk.FileFilter()
		self.XML = File
		# add gtk.Filter
	
	def OpenDialog(self,widget):
		"""OpenDialog method: load anf write audio 
		files
		:return None:"""
		pattern = (".mp3") 	
		self.filtro.set_name("*.mp3")
		for name, pattern in filepattern:
 			self.filtro.add_pattern(pattern)         	
		self.getInstance().add_filter(self.filtro)
		respt=self.getInstance().run()
		self.getInstance().remove_filter(self.filtro)
		self.Hide_()
		dom = minidom.parse(self.XML)
		wml = dom.getElementsByTagName('wml')
		if respt == -5:
			fileselected = self.getInstance().get_filenames()
			for files in fileselected:
				(dirs,files)= os.path.split(files)
				self.getParent().child["media"].append([files,dirs])
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
			xmldocument = open(self.XML,"w")
			dom.writexml(xmldocument)
			xmldocument.close()


	
