#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create importWindow
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

from gi.repository import Gtk
import WindowBase
from xml.dom.minidom import Document
from xml.dom import minidom
import resources
import os
import eyeD3
from mutagen.mp3 import MP3 

filepattern = (("MP3","*.mp3"),) 
"""Sopported formats"""

class importWindow(WindowBase.window):
	"""importWindow class: based on GlmPlayer class
	creates an openDialog window"""

	def __init__(self,builder,parent,File):
		"""initial method: set initial
		values
		:param parent: window parent
		:param builder: Gtk.Builder
		:return: None"""
		WindowBase.window.__init__(self,parent,builder)
		# Base initial Method	
		self.filtro = Gtk.FileFilter()
		self.XML = File
		# add Gtk.Filter
	
	def OpenDialog(self,widget):
		tag = eyeD3.Tag()
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
				nombre = files
				ruta = dirs
				tag.link(ruta+"/"+nombre)
				audio = MP3(ruta+"/"+nombre)
				titulo = ""
				artista = ""
				album = ""
				if tag.getAlbum() != "" and tag.getAlbum() != " ":
					album = tag.getAlbum() 
				else:
					album = "Desconocido"
				if tag.getArtist() != "" and tag.getArtist() != " ":
					artista = tag.getArtist()
				else:
					artista = "Desconocido"
				if tag.getTitle() != "" and tag.getTitle() != " ":
					titulo = tag.getTitle()
				else:
					titulo = nombre
				duration = audio.info.length	
				times = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
				self.getParent().child["media"].append([titulo,album,artista,str(times)+" min",nombre,ruta])
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


	
