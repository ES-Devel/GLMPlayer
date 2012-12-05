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
	"""importWindow class: based on GlmPlayer class
	creates an openDialog window"""

	def __init__(self,builder,parent):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: gtk.Builder
		:return: None"""
		window.Glmplayer.__init__(self,parent,builder)
		# Base initial Method	
		self.filtro = gtk.FileFilter()
		# add gtk.Filter

	def Start(self,name):
		"""Start method: build window (overload)
		:param name: window name to be created
		:return: None"""
		self.instance(self.getBuilder().get_object(name))

	def Set(self):
		"""Set Method: (overload)
		:return: None"""
		pass
	
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
		self.Hide()
		dom = minidom.parse(resources.ConfigFiles()+"track.xml")
		wml = dom.getElementsByTagName('wml')
		if respt == -5:
			fileselected = window.Glmplayer.getInstance().get_filenames()
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


	
