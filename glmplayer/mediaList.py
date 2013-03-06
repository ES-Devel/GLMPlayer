# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from glmplayer_lib import resources,xmllib

from xml.dom.minidom import Document

from xml.dom import minidom 

class MediaList( ):

	def __init__( self , parent , MediaList , MediaTree , File ):
		self.__parent = parent
		self.List = MediaList
		self.Tree = MediaTree
		self.XML = File
		self.xml_parser = xmllib.xml_parser(self.XML,'glmplayer')
	
	def Search(self):
		num = len(self.xml_parser.get_list_of_elements('pista'))
		i = 0
		while i < num:
		    name = resources.clearing(self.xml_parser.search_value_by_pos('file',i))
            search_path = resources.clearing(self.xml_parser.search_value_by_pos('path',i))
            titulo = resources.clearing(self.xml_parser.search_value_by_pos('title',i))
            album = resources.clearing(self.xml_parser.search_value_by_pos('album',i))
            artista = resources.clearing(self.xml_parser.search_value_by_pos('artist',i))
            duration = float(resources.clearing(self.xml_parser.search_value_by_pos('duration',i)))
            full_path = search_path+'/'+name
	    	times = int(duration/60)+float(int((float(duration/60)-int(duration/60))*60))/100
			self.List.append([titulo,album,artista,str(times)+" min",name,search_path])
            i = i + 1

	def delete(self,widget):
		select=self.Tree.get_selection()
		filepath=resources.on_tree_selection_changed(select)
		(modelo,filas)=select.get_selected_rows()
		for i in filas:
			val = int(resources.cleanNode(i))
			iterador=modelo.get_iter(i)
		treeiter=self.List.remove(iterador)
		self.xml_parser.delete_by_terms('pista','title',filepath)
		self.xml_parser.update_xml()
	
	def clean(self,widget):
		self.xml_parser.reset_but_keep_root('glmplayer')
		self.List.clear()
		
	
	def get_row_value(self,col,tag):
	    select=self.Tree.get_selection()
		filepath=resources.on_tree_selection_changed(select)
		return self.xml_parser.get_value_by_terms(tag,col,filepath,len(self.xml_parser.get_list_of_elements(tag)))
		
	def set_row_value(self,col,tag,value):
	    select=self.Tree.get_selection()
		filepath=resources.on_tree_selection_changed(select)
		self.xml_parser.set_value_by_terms(tag,col,filepath,len(self.xml_parser.get_list_of_elements(tag)),value)
