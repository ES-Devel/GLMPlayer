#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create MediaList
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

from xml.dom.minidom import Document
from xml.dom import minidom
import resources

class MediaList():
	def __init__(self,parent):
		self.__parent = parent
	
	def Search(self):
		try:
			dom = minidom.parse(resources.ConfigFiles()+"track.xml")
			for i in range(0,len(dom.getElementsByTagName("track"))):
				self.__parent.medialist.append([resources.clearing\
				(dom.getElementsByTagName("track")[i].firstChild.data),resources.clearing\
				(dom.getElementsByTagName("ruta")[i].firstChild.data)])
        	except:
			pass

	def delete(self,widget):
		"""delete selected file from playlist"""
		try:
			select = self.__parent.tree.get_selection()
			filepath = resources.on_tree_selection_changed(select)
			(modelo,filas) = select.get_selected_rows()
			for i in filas:
					for token in i:
						if token == '(' or token == ' ' or token == ',' or token == ')':
							pass
						else:
							node = token
					val = int(node)
					iterador = modelo.get_iter(i)
			treeiter = self.__parent.medialist.remove(iterador)
			dom = minidom.parse(resources.ConfigFiles()+"track.xml")
			found = -1
			for i in range(0,len(dom.getElementsByTagName("track"))):
				if filepath.find(dom.getElementsByTagName("track")[i].firstChild.data) >= 0:
					found = i
			dom.getElementsByTagName("wml")[0].removeChild(dom.getElementsByTagName("pista")[found])
			xmldocument = open(resources.ConfigFiles()+"track.xml","w")
			dom.writexml(xmldocument)
			xmldocument.close()
		except:
			pass
	
	def clean(self,widget):
		"""clean playlist"""
		doc = open(resources.ConfigFiles()+"track.xml","w")
		doc.write('<?xml version="1.0" ?><wml></wml>')
		doc.close()
		self.__parent.medialist.clear()
