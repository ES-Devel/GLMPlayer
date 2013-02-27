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
# with this program.  If not, see <http://www.gfrom gi.repository import Gtknu.org/licenses/>.
### END LICENSE

from gi.repository import Gtk,GdkPixbuf,Gdk 

from glmplayer_lib import resources, glmplayerconfig

import random

import gst

try:
	from mutagen import File

	from mutagen.mp3 import MP3

	from mutagen.id3 import ID3, APIC, error
	
	import eyeD3
	
except ImportError:
	pass 

class Stream():
	def __init__( self, parent, param_artwork, progressBar, MediaTree, metadatahandler ):

			self.__parent__ = parent
			self.player = gst.element_factory_make( "playbin2", "player" )
									
			self.ProgressBar = progressBar
			self.tmp_artwork = param_artwork
			self.Tree = MediaTree
			self.resourcesImg = glmplayerconfig.get_data_path()+"/ui/artwork.png"
			self.resourcesNoImg = glmplayerconfig.get_data_path()+"/ui/NOCD.png"
			self.metadatahandler = metadatahandler
			
			self.MAPA = [] 
			self.current = 0
			self.controler = 0
			self.max = 0
			self.time_song = 0
        
	def core(self):
		self.stop_state( )
		select = self.Tree.get_selection(	)
		fileresources = resources.on_tree_selection_changed( select	)
		
		try:
			tag = eyeD3.Tag	( )
			audio = MP3	( fileresources )
			tag.link	( fileresources )
		except:
			print "Formato de pista incorrecto"
		
		self.loadArtwork( DATA = File( fileresources ))
		
		duration = audio.info.length
		fileLen = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
		
		self.metadatahandler.UpdateMetaData( metaData = tag, time = fileLen )	
		
		model, treeiter = select.get_selected(	)
		
		self.player.set_property( "uri", "file://"+fileresources )		
		self.player.set_state( gst.STATE_PLAYING )
		
		return duration                              

	def play_state(self):
		if self.controler == 1:
			self.player.set_state( gst.STATE_PLAYING )
			self.controler = 0
		else:
			select = self.Tree.get_selection( )
			( modelo , filas ) = select.get_selected_rows( )
			contador = 0
			val = 0
			node = " "
			for i in filas:
				val = int( resources.cleanNode ( i ) )
				iterador = modelo.get_iter( 0 )
				while iterador != None:
					iterador = modelo.iter_next( iterador )
					contador = contador + 1
				contador
			if self.__parent__.child["random"].get_active( ) == False:
				self.MAPA = range(val,contador)
				self.current = 1
			else:
				self.MAPA = range	( 0 ,contador )
				random.shuffle		( self.MAPA )
				self.current = 0
			self.max = contador
			
		    return self.core( ), "Now Playing"
	
	def next_state(self): 
		try:	 
			select = self.Tree.get_selection( )
			( modelo , filas ) = select.get_selected_rows(	)
			iterador = modelo.get_iter( self.MAPA[self.current] )
			select.select_iter( iterador )
			self.current = self.current + 1
			return self.core( ), "Now Playing"
		except:
			if self.__parent__.child["repeat"].get_active(  ) == False:
				self.player.set_state( gst.STATE_NULL ) 
			else:
				self.current = 0
				select = self.Tree.get_selection(  )
				( modelo , filas ) = select.get_selected_rows( )
				iterador = modelo.get_iter( self.MAPA[self.current] )
				select.select_iter( iterador )
				self.current = self.current + 1
				return self.core(  ), "Now Playing"
		self.controller = 0
	
	def prev_state(self):
		if self.MAPA[self.current] < 0:
			pass
		else:
			self.current = self.current - 1	
			select = self.Tree.get_selection(	)
			( modelo , filas ) = select.get_selected_rows( )
			iterador = modelo.get_iter( self.MAPA[self.current] )
			select.select_iter(iterador)
			return self.core( ), "Now Playing"
		self.controller = 0

	def stop_state(self):	
		self.player.set_state( gst.STATE_NULL )
		self.controller = 0
		return "Stop"
		
	def pause_state(self):
		self.player.set_state( gst.STATE_PAUSED )	
		self.controler = 1
		return "Paused"
		
	def loadArtwork(self, DATA):
		CHOOSEN = None
		try:
			artwork = DATA.tags['APIC:'].data 
			with open( self.resourcesImg, 'wb' ) as img:
				img.write( artwork )
			CHOOSEN = self.resourcesImg
		except:
			CHOOSEN = self.resourcesNoImg
		try:	
			self.tmp_artwork.set_from_pixbuf( GdkPixbuf.Pixbuf.new_from_file_at_size( CHOOSEN, 50, 50 ) )
		except:
			print "No se puede cargar la imagen"
