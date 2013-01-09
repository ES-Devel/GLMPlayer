# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 <William Parras> <william.parras.mendez@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from glmplayer_lib import resources

from xml.dom.minidom import Document

from xml.dom import minidom 

try:
	import eyeD3
except ImportError:
	pass
try:
    from mutagen.mp3 import MP3 
except ImportError:
	pass
 

class MediaList( ):
	def __init__( self , parent , MediaList , MediaTree , File ):
		self.__parent = parent
		self.List = MediaList
		self.Tree = MediaTree
		self.XML = File
	
	def Search(self):
	    __numErrors__ = 0
        __errorLog__ = []
		tag = eyeD3.Tag	( )
		dom = minidom.parse( self.XML )
		num = len( dom.getElementsByTagName("pista") )
		i = 0
		while i < num:
		    nombre = resources.clearing ( 
				    		dom.getElementsByTagName("track")[i].firstChild.data
				    	)
				    	
            ruta = resources.clearing (
			    			dom.getElementsByTagName("ruta")[i].firstChild.data
			    		)
		    try:			
		    	tag.link( ruta+"/"+nombre )
	    		audio = MP3	( ruta+"/"+nombre )
			
	    		titulo = nombre
    			artista = "Desconocido"
	    		album = "Deconocido"
			
	    		if tag.getAlbum( ) != "" and tag.getAlbum( ) != " ":
	    			album = tag.getAlbum( ) 
				
	    		if tag.getArtist( ) != "" and tag.getArtist( ) != " ":
	    			artista = tag.getArtist( )
			
	    		if tag.getTitle( ) != "" and tag.getTitle( ) != " ":
	    			titulo = tag.getTitle( )
			
	    		duration = audio.info.length
				
	    		times = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
				
	    		self.List.append (
	    		[ titulo , album , artista , str(times)+" min" , nombre , ruta ]
	    				)
			
	    	except:
	    	    __numErrors__ = __numErrors__ + 1
	    	    __errorLog__.append("file//:"+ruta+"/"+nombre+"  Not Found")

            i = i + 1
            
        return __numErrors__, __errorLog__

	def delete(self,widget):
		try:
			select = self.Tree.get_selection				(   )
			filepath = resources.on_tree_selection_changed	( select )
			( modelo , filas ) = select.get_selected_rows	(   )
			
			for i in filas:
				val = int( resources.cleanNode ( i ) )
				iterador = modelo.get_iter ( i )
					
			treeiter = self.List.remove ( iterador )
			dom = minidom.parse 		( self.XML )
			found = -1
			for i in range( 0, len ( dom.getElementsByTagName("track") ) ):
				if filepath.find( dom.getElementsByTagName("track")[i].firstChild.data ) >= 0:
					found = i
			dom.getElementsByTagName("wml")[0].removeChild( dom.getElementsByTagName("pista")[found] )
			xmldocument = open	( self.XML , "w" )
			dom.writexml		( xmldocument )
			xmldocument.close(  )
		except:
			pass
	
	def clean(self,widget):
		doc = open	   ( self.XML , "w" )
		doc.write	   ('<?xml version="1.0" ?><wml></wml>')
		doc.close	   (  )
		self.List.clear(  )
