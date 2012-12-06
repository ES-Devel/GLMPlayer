#!/usr/bin/env python

import gst
import gtk
import ThreadStream
import path
import eyeD3
from mutagen import File
from mutagen.mp3 import MP3 
from mutagen.mp3 import MPEGInfo 
from mutagen.id3 import ID3, APIC, error 

class Stream():
	def __init__(self,parent,param_artwork,progressBar,MediaTree,img,Noimg,\
	statusBar,artist,album,duration,title):
			self.__parent__ = parent
			self.player = gst.element_factory_make("playbin2", "player")
			bus = self.player.get_bus()
			bus.add_signal_watch()
			bus.enable_sync_message_emission()
			bus.connect("message", self.on_message)
			bus.connect("sync-message::element", self.on_sync_message)
			self.hilo = ThreadStream.RepThread(0,progressBar,1)
			self.ProgressBar = progressBar
			self.tmp_artwork = param_artwork
			self.Tree = MediaTree
			self.pathImg = img
			self.pathNoImg = Noimg
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
		self.stop_state()
		select = self.Tree.get_selection()
		filepath = path.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		audio = MP3(filepath)
		try:
			artwork = file_t.tags['APIC:'].data 
			with open(self.pathImg, 'wb') as img:
				img.write(artwork)
			self.tmp_artwork.set_from_pixbuf(\
			gtk.gdk.pixbuf_new_from_file_at_size(self.pathImg, 200, 200))
		except:
			self.tmp_artwork.set_from_pixbuf(\
			gtk.gdk.pixbuf_new_from_file_at_size(self.pathNoImg, 200, 200))
		
		duration = audio.info.length
		times = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
		tag.link(filepath)
		self.StatusBar.push(self.StatusBar.get_context_id("playing"),"Now playing")
		self.Artist.set_text(tag.getArtist())
		self.Album.set_text(tag.getAlbum())
		self.Duration.set_text("%.2f" % times + "  min")
		self.Title.set_text(tag.getTitle())
		self.player.set_property("uri", "file://"+filepath)
		self.hilo = ThreadStream.RepThread(duration,self.ProgressBar,1)
		self.hilo.start()
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
			self.StatusBar.push(self.StatusBar.get_context_id("Error"),"Error: somethig went wrong")
                                                             
	def on_sync_message(self, bus, message):
		if message.structure is None:
			return
		message_name = message.structure.get_name()
		if message_name == "prepare-xwindow-id":
			imagesink = message.src
			imagesink.set_property("force-aspect-ratio", True)
			gtk.gdk.threads_enter()
			imagesink.set_xwindow_id(self.__parent__.movie_window.window.xid)
			gtk.gdk.threads_leave()

	def play_state(self):
		if self.controler == 1:
			self.player.set_state(gst.STATE_PLAYING)
			self.StatusBar.push(self.StatusBar.get_context_id("playing"),"Now playing")
			self.hilo = ThreadStream.RepThread(self.dur,\
			self.ProgressBar,self.state)
			self.hilo.start()
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
				iterador = modelo.get_iter(i)
				while iterador != None:
					iterador = modelo.iter_next(iterador)
					contador = contador + 1
			self.MAPA = path.ObtenerLista(contador,val)
			self.max = contador
			self.current = 1
			self.core()
	
	def next_state(self): 
		try:	 
			select = self.Tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(self.MAPA[self.current])
		except: 
			self.current = 0
			select = self.Tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(self.MAPA[self.current])
		select.select_iter(iterador)
		self.core()
		self.current = self.current + 1
	
	def prev_state(self):
		if self.current <= 0:
			pass
		else:
			self.current = self.current - 1	
			select = self.Tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(self.MAPA[self.current])
			select.select_iter(iterador)
			self.core()	

	def stop_state(self):	
		self.player.set_state(gst.STATE_NULL)
		self.StatusBar.push(self.StatusBar.get_context_id("Stop"),"Stop")
		self.hilo.stop()
		
	def pause_state(self):
		self.player.set_state(gst.STATE_PAUSED)
		self.StatusBar.push(self.StatusBar.get_context_id("pause"),"Paused")
		self.state,self.dur = self.hilo.pause()	
		self.controler = 1

	def KILL(self):
		self.hilo.stop()
