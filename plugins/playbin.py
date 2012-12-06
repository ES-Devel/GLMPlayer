#!/usr/bin/env python

import gst
import ThreadStream
import path
import eyeD3
from mutagen import File
from mutagen.mp3 import MP3 
from mutagen.mp3 import MPEGInfo 
from mutagen.id3 import ID3, APIC, error 
from cStringIO import StringIO

class Stream():
	def __init__(self,parent):
	        self.__parent__ = parent
	        parent.player = gst.element_factory_make("playbin2", "player")
	        bus = parent.player.get_bus()
	        bus.add_signal_watch()
	        bus.enable_sync_message_emission()
	        bus.connect("message", self.on_message)
	        bus.connect("sync-message::element", self.on_sync_message)
	        parent.hilo = ThreadStream.RepThread(0,parent.progressBar,1)
        
	def core(self):
		self.stop_state()
		select = self.__parent__.tree.get_selection()
		filepath = path.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		audio = MP3(filepath)
		try:
			artwork = file_t.tags['APIC:'].data 
			with open(path.icons+'artwork.png', 'wb') as img:
				img.write(artwork)
			self.__parent__.imagen.set_from_pixbuf(\
			gtk.gdk.pixbuf_new_from_file_at_size(path.icons+'artwork.png', 200, 200))
		except:
			self.__parent__.imagen.set_from_file(path.icons+"NOCD.png")
		
		duration = audio.info.length
		times = int(duration/60) + float(int((float(duration/60) - int(duration/60))*60))/100
		tag.link(filepath)
		self.__parent__.info.push(self.__parent__.info.get_context_id("playing"),"Now playing")
		self.__parent__.artista.set_text(tag.getArtist())
		self.__parent__.album.set_text(tag.getAlbum())
		self.__parent__.duracion.set_text("%.2f" % times + "  min")
		self.__parent__.titulo.set_text(tag.getTitle())
		self.__parent__.player.set_property("uri", "file://"+filepath)
		self.__parent__.hilo = ThreadStream.RepThread(duration,self.__parent__.progressBar,1)
		self.__parent__.hilo.start()
		self.__parent__.player.set_state(gst.STATE_PLAYING)

	def on_message(self, bus, message):
		t = message.type 
		if t == gst.MESSAGE_EOS: 
			self.__parent__.player.set_state(gst.STATE_NULL)
			self.__parent__.next_state()
		elif t == gst.MESSAGE_ERROR:
			self.__parent__.player.set_state(gst.STATE_NULL)
			err, debug = message.parse_error()
			print "Error: %s" % err, debug
			self.info.push(self.__parent__.info.get_context_id("Error"),"Error: somethig went wrong")
                                                             
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
		if self.__parent__.controler == 1:
			self.__parent__.player.set_state(gst.STATE_PLAYING)
			self.__parent__.info.push(self.__parent__.info.get_context_id("playing"),"Now playing")
			self.__parent__.hilo = ThreadStream.RepThread(self.__parent__.dur,\
			self.__parent__.progressBar,self.__parent__.state)
			self.__parent__.hilo.start()
			self.__parent__.controler = 0
		else:
			select = self.__parent__.tree.get_selection()
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
			self.__parent__.MAPA = path.ObtenerLista(contador,val)
			self.__parent__.max = contador
			self.__parent__.current = 1
			self.__parent__.gst_builder.core()
	
	def next_state(self): 
		try:	 
			select = self.__parent__.tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(self.__parent__.MAPA[self.__parent__.current])
		except: 
			self.__parent__.current = 0
			select = self.__parent__.tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(self.__parent__.MAPA[self.__parent__.current])

		select.select_iter(iterador)
		self.__parent__.gst_builder.core()
		self.__parent__.current = self.__parent__.current + 1
	
	def prev_state(self):
		if self.__parent__.current <= 0:
			pass
		else:
			self.__parent__.current = self.__parent__.current - 1	
			select = self.__parent__.tree.get_selection()
			(modelo,filas) = select.get_selected_rows()
			iterador = modelo.get_iter(self.__parent__.MAPA[self.__parent__.current])
			select.select_iter(iterador)
			self.__parent__.gst_builder.core()	

	def stop_state(self):	
		self.__parent__.player.set_state(gst.STATE_NULL)
		self.__parent__.info.push(self.__parent__.info.get_context_id("Stop"),"Stop")
		self.__parent__.hilo.stop()
		
	def pause_state(self):
		self.__parent__.player.set_state(gst.STATE_PAUSED)
		self.__parent__.info.push(self.__parent__.info.get_context_id("pause"),"Paused")
		self.__parent__.state,self.__parent__.dur = self.__parent__.hilo.pause()	
		self.__parent__.controler = 1
