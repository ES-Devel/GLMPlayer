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

from glmplayer_lib import WindowBase, resources

from gi.repository import Gtk

from xml.dom.minidom import Document

from xml.dom import minidom

import os

try:
	import eyeD3
except ImportError:
	print "To run this program correctly you must install python-eyed3"

try:
    from mutagen.mp3 import MP3 
except ImportError:
	print "To run this program correctly you must install mutagen" 
	
filepattern = ( ("MP3","*.mp3") ,) 

class importWindow( WindowBase.window ):

	def __init__( self , builder , parent , File ):
		WindowBase.window.__init__	( self , parent , builder )	
		self.filtro = Gtk.FileFilter(  )
		self.XML = File
	
	def OpenDialog(self,widget):
		tag = eyeD3.Tag 	(  )
		pattern = 			(".mp3") 	
		self.filtro.set_name("*.mp3")
		
		for name, pattern in filepattern:
 			self.filtro.add_pattern ( pattern )
 			         	
		self.getInstance( ).add_filter	 ( self.filtro )
		respt=self.getInstance( ).run	 (  )
		self.getInstance( ).remove_filter( self.filtro )
		
		self.Hide_( )
		
		dom = minidom.parse( self.XML )
		wml = dom.getElementsByTagName ('wml')
		
		if respt == -5:
			fileselected = self.getInstance( ).get_filenames	( )
			for files in fileselected:
				( dirs , files )= os.path.split( files )
				nombre = files
				ruta = dirs
				
				tag.link	( ruta+"/"+nombre )
				audio = MP3	( ruta+"/"+nombre )
				
				titulo = nombre
				artista = "Desconocido"
				album = "Desconocido"
				
				if tag.getAlbum( ) != "" and tag.getAlbum( ) != " ":
					album = tag.getAlbum( ) 
					
				if tag.getArtist( ) != "" and tag.getArtist( ) != " ":
					artista = tag.getArtist( )
				
				if tag.getTitle( ) != "" and tag.getTitle( ) != " ":
					titulo = tag.getTitle( )
					
				duration = audio.info.length
					
				time_ = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
				self.getParent( ).child["media"].append(
					[ titulo , album , artista , str(time_)+" min" , nombre , ruta ]
				)
				
				maincard = dom.createElement	( "pista"  )
				wml[0].appendChild				( maincard )
				nm = dom.createElement			( "track"  )
				maincard.appendChild			( nm 	   )
				nombre = dom.createTextNode		( files    )
				nm.appendChild					( nombre   )
				dr = dom.createElement			( "ruta"   )
				maincard.appendChild			( dr  	   )
				paths = dom.createTextNode		( dirs     )
				dr.appendChild					( paths    )
				
			xmldocument = open( self.XML , "w" )
			dom.writexml( xmldocument )
			xmldocument.close(  )


	
