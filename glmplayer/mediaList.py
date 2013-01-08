# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from glmplayer_lib import resources

from xml.dom.minidom import Document

from xml.dom import minidom

try:
	import eyeD3
except ImportError:
	print "To run this program correctly you must install python-eyed3"

try:
    from mutagen.mp3 import MP3 
except ImportError:
	print "To run this program correctly you must install mutagen"
 

class MediaList( ):
	def __init__( self , parent , MediaList , MediaTree , File ):
		self.__parent = parent
		self.List = MediaList
		self.Tree = MediaTree
		self.XML = File
	
	def Search(self):
		tag = eyeD3.Tag	( )
		try:
		    dom = minidom.parse( "data/config/"+self.XML )
		    self.backup = "data/config/"+self.XML
		except:
		    dom = minidom.parse( "/usr/local/share/Glmplayer/config/"+self.XML )
		    self.backup = "/usr/local/share/Glmplayer/config/"+self.XML
		num = len( dom.getElementsByTagName("pista") )
		i = 0
		while i < num:
		    try:
			    nombre = resources.clearing ( 
				    		dom.getElementsByTagName("track")[i].firstChild.data
				    	)
				    	
			    ruta = resources.clearing (
			    			dom.getElementsByTagName("ruta")[i].firstChild.data
			    		)		
					
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
	    	    print "hay archivos perdidos"

            i = i + 1

	def delete(self,widget):
		try:
			select = self.Tree.get_selection				(   )
			filepath = resources.on_tree_selection_changed	( select )
			( modelo , filas ) = select.get_selected_rows	(   )
			
			for i in filas:
				val = int( resources.cleanNode ( i ) )
				iterador = modelo.get_iter ( i )
					
			treeiter = self.List.remove ( iterador )
			dom = minidom.parse 		( self.backup )
			found = -1
			for i in range( 0, len ( dom.getElementsByTagName("track") ) ):
				if filepath.find( dom.getElementsByTagName("track")[i].firstChild.data ) >= 0:
					found = i
			dom.getElementsByTagName("wml")[0].removeChild( dom.getElementsByTagName("pista")[found] )
			xmldocument = open	( self.backup , "w" )
			dom.writexml		( xmldocument )
			xmldocument.close(  )
		except:
			pass
	
	def clean(self,widget):
		doc = open	   ( self.backup , "w" )
		doc.write	   ('<?xml version="1.0" ?><wml></wml>')
		doc.close	   (  )
		self.List.clear(  )
