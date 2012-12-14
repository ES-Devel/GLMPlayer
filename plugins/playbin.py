#!/usr/bin/env python

import gst
from gi.repository import Gtk,GdkPixbuf,Gdk
from core import resources
import eyeD3
import random
from mutagen import File
from mutagen.mp3 import MP3 
from mutagen.mp3 import MPEGInfo 
from mutagen.id3 import ID3, APIC, error 
import dbus

bus = dbus.SessionBus()
notify_object = bus.get_object(
			'org.freedesktop.Notifications',
			'/org/freedesktop/Notifications'
			)
			
notify_interface = dbus.Interface(
			notify_object,
			'org.freedesktop.Notifications'
			)


class Stream():
	def __init__(
			self,
			parent,
			param_artwork,
			progressBar,
			MediaTree,
			img,
			Noimg,
			statusBar,
			artist,
			album,
			duration,
			title
		):
			self.__parent__ = parent
			
			self.player = gst.element_factory_make(
								"playbin2",
								 "player"
							)
							
			bus = self.getBus()
									
			self.ProgressBar = progressBar
			self.tmp_artwork = param_artwork
			self.Tree = MediaTree
			self.resourcesImg = img
			self.resourcesNoImg = Noimg
			self.StatusBar = statusBar
			
			self.MAPA = [] 
			self.current = 0
			self.controler = 0
			self.max = 0
			self.time_song = 0
			
			self.Artist = artist
			self.Album = album
			self.Title = title
			self.Duration = duration 
        
	def core(self):
		
		try:
			self.stop_state()
		except:
			pass
			
		select = self.Tree.get_selection()
		fileresources = resources.on_tree_selection_changed(select)
		
		try:
			tag = eyeD3.Tag()
			audio = MP3(fileresources)
			tag.link(fileresources)
		except:
			print "No se puede obtener informacion sobre esta pista"
		
		self.loadArtwork(
				DATA = File(fileresources)
			)
		
		duration = audio.info.length
		fileLen = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
		
		self.StatusBar.push(
				self.StatusBar.get_context_id("playing"),
				"Now playing"
				)
		
		self.UpdateMetaData(
			metaData = tag,
			time = fileLen
		)	
		
		model, treeiter = select.get_selected()
		
		notify_id = notify_interface.Notify(
				"DBus Test",
				 0,
				 "",
				 model[treeiter][0],
				 "por "+model[treeiter][2]+" de "+model[treeiter][1],
				 "",
				 { },
				 100
			)
		
		self.player.set_property(
					"uri",
					"file://"+fileresources
				)
				
		self.player.set_state(gst.STATE_PLAYING)

	def on_message(self, bus, message):
		t = message.type 
		if t == gst.MESSAGE_EOS: 
			self.player.set_state(gst.STATE_NULL)
			self.next_state()
		elif t == gst.MESSAGE_ERROR:
			self.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.StatusBar.push(
						self.StatusBar.get_context_id("Error"),
						"Error: somethig went wrong"
					)
    
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			Gdk.threads_enter()
			imagesink.set_xwindow_id(self.__parent__.movie_window.window.xid)
			Gdk.threads_leave()                                                       

	def play_state(self):
		if self.controler == 1:
			self.player.set_state(gst.STATE_PLAYING)
			self.StatusBar.push(
						self.StatusBar.get_context_id("playing"),
						"Now playing"
					)
			self.hilo = ThreadStream.RepThread(
					self.dur,
					self.ProgressBar,
					self.state
				)
			self.controler = 0
		else:
			select = self.Tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			contador = 0
			val = 0
			node = " "
			for i in filas:
				for token in i:
					if token == '(' or token == ' ' or token == ',' or token == ')':
						pass
					else:
						node = token
				val = int(node)
				iterador = modelo.get_iter(0)
				while iterador != None:
					iterador = modelo.iter_next(iterador)
					contador = contador + 1
				contador
			if self.__parent__.child["random"].get_active() == False:
				self.MAPA = range(val,contador)
				self.current = 1
			else:
				self.MAPA = range(0,contador)
				random.shuffle(self.MAPA)
				self.current = 0
			self.max = contador
			try:
				self.core()
			except:
				pass
	
	def next_state(self): 
		try:	 
			select = self.Tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(
					self.MAPA[self.current]
					)
			select.select_iter(iterador)
			self.current = self.current + 1
			self.core()
		except:
			if self.__parent__.child["repeat"].get_active() == False:
				self.player.set_state(gst.STATE_NULL) 
			else:
				self.current = 0
				select = self.Tree.get_selection()
				(modelo,filas) = select.get_selected_rows()
				iterador = modelo.get_iter(
						self.MAPA[self.current]
						)
				select.select_iter(iterador)
				self.current = self.current + 1
				try:
					self.core()
				except:
					pass
	
	def prev_state(self):
		try:
			if self.MAPA[self.current] <= 0:
				pass
			else:
				self.current = self.current - 1	
				select = self.Tree.get_selection()
				(modelo,filas) = select.get_selected_rows()
				iterador = modelo.get_iter(
								self.MAPA[self.current]
								)
				select.select_iter(iterador)
				try:
					self.core()
				except:
					pass
		except:
			pass	

	def stop_state(self):	
		self.player.set_state(gst.STATE_NULL)
		self.StatusBar.push(
				self.StatusBar.get_context_id("Stop"),
				"Stop"
				)
		
	def pause_state(self):
		self.player.set_state(gst.STATE_PAUSED)
		self.StatusBar.push(
				self.StatusBar.get_context_id("pause"),
				"Paused"
				)	
		self.controler = 1
		
	def loadArtwork(self, DATA):
		CHOOSEN = None
		try:
			artwork = DATA.tags['APIC:'].data 
			with open(self.resourcesImg, 'wb') as img:
				img.write(artwork)
			CHOOSEN = self.resourcesImg
		except:
			CHOOSEN = self.resourcesNoImg
		try:	
			self.tmp_artwork.set_from_pixbuf(
				GdkPixbuf.Pixbuf.new_from_file_at_size(
									CHOOSEN,
									 200,
									 200
								)
							)
		except:
			print "No se puede cargar la imagen"
						
	def UpdateMetaData(self, metaData, time):
		self.Artist.set_text(metaData.getArtist())
		self.Album.set_text(metaData.getAlbum())
		self.Duration.set_text("%.2f" % time + "  min")
		self.Title.set_text(metaData.getTitle())
		
	def getBus(self):
		bus = self.player.get_bus()
		bus.add_signal_watch()
		bus.enable_sync_message_emission()
		bus.connect(
			"message",
			 self.on_message
			 )
		bus.connect(
			"sync-message::element",
			 self.on_sync_message
			 )
		return bus
		
