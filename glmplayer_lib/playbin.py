# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

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
			
			'allow user to use mediaList using or not using random method'
			self.MAPA = [] 
			self.current = 0
			self.controler = 0
			self.max = 0
			self.time_song = 0
        
	def core(self):
	    'every time core is called stop every activity'
		self.stop_state( )
		'gets tree selection'
		select = self.Tree.get_selection(	)
		'clear path'
		fileresources = resources.on_tree_selection_changed( select	)
		try:
			tag = eyeD3.Tag	( )
			audio = MP3	( fileresources )
			tag.link	( fileresources )
			duration = audio.info.length
		    fileLen = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
		except:
		    duration = 0
		    fileLen = 0
		    tag = None
			print "glmplayer 0.1 only supports MP3"
		'load artwork using tree selection path'
		self.loadArtwork( DATA = File( fileresources ))
		'uptade gui with metadata info'
		self.metadatahandler.UpdateMetaData( metaData = tag, time = fileLen )	
		model, treeiter = select.get_selected(	)
		'start playing'
		self.player.set_property( "uri", "file://"+fileresources )		
		self.player.set_state( gst.STATE_PLAYING )	
		'return file length'
		return duration                              

	def play_state(self):
	    'check if paused'
		if self.controler == 1:
		    'yeah! is paused, lets play'
			self.player.set_state( gst.STATE_PLAYING )
			self.controler = 0
		else:
		    'if not paused, well we will make a sort'
		    'get tree selection'
			select = self.Tree.get_selection( )
			( modelo , filas ) = select.get_selected_rows( )
			contador = 0
			val = 0
			node = " "
			for i in filas:
			    'this will get a number pointing to selected row'
				val = int( resources.cleanNode ( i ) )
				iterador = modelo.get_iter( 0 )
				'now we will count how many songs are listed'
				while iterador != None:
					iterador = modelo.iter_next( iterador )
					contador = contador + 1
				'we got it'
				contador
			'if random is false'
			if self.__parent__.child["random"].get_active( ) == False:
			    'list values for playlist'
				self.MAPA = range(0,contador)
				self.current = val
			else:
			    'make the same but shuffle'
				self.MAPA = range( 0 ,contador )
				random.shuffle	 ( self.MAPA )
				self.current = 0
			'max value'
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
	    'send null to pipeline'	
		self.player.set_state( gst.STATE_NULL )
		self.controller = 0
		return "Stop"
		
	def pause_state(self):
	    'pause current song'
		self.player.set_state( gst.STATE_PAUSED )	
		self.controler = 1
		return "Paused"
		
	def loadArtwork(self, DATA):
		CHOOSEN = None
		try:
		    'read APIC frames'
			artwork = DATA.tags['APIC:'].data
			'use frames to create artwork' 
			with open( self.resourcesImg, 'wb' ) as img:
				img.write( artwork )
			'choose artwork'
			CHOOSEN = self.resourcesImg
		except:
		    'if not APIC frames use default image'
			CHOOSEN = self.resourcesNoImg
		try:	
			self.tmp_artwork.set_from_pixbuf( GdkPixbuf.Pixbuf.new_from_file_at_size( CHOOSEN, 50, 50 ) )
		except:
			print "No se puede cargar la imagen"
