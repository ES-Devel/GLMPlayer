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
	def __init__(self,parent,MediaList,MediaTree,File):
		self.__parent = parent
		self.List = MediaList
		self.Tree = MediaTree
		self.XML = File
	
	def Search(self):
		try:
			dom = minidom.parse(self.XML)
			for i in range(0,len(dom.getElementsByTagName("track"))):
				self.List.append([resources.clearing\
				(dom.getElementsByTagName("track")[i].firstChild.data),resources.clearing\
				(dom.getElementsByTagName("ruta")[i].firstChild.data)])
        	except:
			pass

	def delete(self,widget):
		"""delete selected file from playlist"""
		try:
			select = self.Tree.get_selection()
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
			treeiter = self.List.remove(iterador)
			dom = minidom.parse(self.XML)
			found = -1
			for i in range(0,len(dom.getElementsByTagName("track"))):
				if filepath.find(dom.getElementsByTagName("track")[i].firstChild.data) >= 0:
					found = i
			dom.getElementsByTagName("wml")[0].removeChild(dom.getElementsByTagName("pista")[found])
			xmldocument = open(self.XML,"w")
			dom.writexml(xmldocument)
			xmldocument.close()
		except:
			pass
	
	def clean(self,widget):
		"""clean playlist"""
		doc = open(self.XML,"w")
		doc.write('<?xml version="1.0" ?><wml></wml>')
		doc.close()
		self.List.clear()
