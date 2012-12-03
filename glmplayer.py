#!/usr/bin/env python

import gtk
import path
import os
from xml.dom.minidom import Document
from xml.dom import minidom
import random
import gst
import subprocess
import eyeD3
import mutagen
from mutagen import File
from mutagen.mp3 import MP3 
from mutagen.id3 import ID3, APIC, error 
from plugins import playbin

filepattern = (("MP3","*.mp3"),) 
"""Sopported formats"""

class main:
	"""main class"""
	def __init__(self):
		"""init method"""
		builder = gtk.Builder()
		builder.add_from_file(path.PATH)  
		"""main window instance"""     		
		
		# Conect aux windows
        	self.agregar_ventana = builder.get_object("Add")
        	self.help = builder.get_object("About")
       		self.window_edicion = builder.get_object("edit")
		
		# Search for objects on windows
        	self.tree = builder.get_object("arbol_pistas")
        	self.medialist = builder.get_object("media")
        	self.sel = builder.get_object("selec")
        	self.imagen = builder.get_object("caratula")
        	self.info = builder.get_object("info")
        	self.artista = builder.get_object("artista")
        	self.album = builder.get_object("album")
        	self.titulo = builder.get_object("titulo")
        	self.duracion = builder.get_object("duracion")
        	self.volumen = builder.get_object("volumen")
        	self.progressBar = builder.get_object("bar")
        	self.stock_interp = builder.get_object("stock_interp")
       		self.stock_titulo = builder.get_object("stock_titulo")
        	self.stock_album = builder.get_object("stock_album")
		

		self.gst_builder = playbin.Stream(self)
		"""get gstreamer controler"""		

        	self.info.set_text("No se ha reproducido nada aun")

        	self.filtro = gtk.FileFilter()
		
		# Search for files on playlist
        	try:
			dom = minidom.parse(path.TRACK)
			for i in range(0,len(dom.getElementsByTagName("track"))):
				self.medialist.append([path.clearing\
				(dom.getElementsByTagName("track")[i].firstChild.data),path.clearing\
				(dom.getElementsByTagName("ruta")[i].firstChild.data)])
        	except:
			pass
		
		# init some info 
        	self.time_song = 0
        	self.imagen.set_from_file(path.icons+"NOCD.png")
		
		# playlist var
        	self.MAPA = [] 
        	self.current = 0
        	self.controler = 0
        	self.max = 0
		
        	dict = {"on_agregar_activate": self.abrir_archivos,
		"gtk_main_quit":self.destroy,
		"on_delete_clicked":self.delete,
		"on_play_clicked":self.play,
		"on_pause_clicked":self.pause,
		"on_prev_clicked":self.prev,
		"on_next_clicked":self.next,
		"on_stop_clicked":self.stop,
		"on_ayud_activate":self.about,
		"on_about_tool_clicked":self.about,
		"on_clean_clicked":self.clean,
		"on_close_about_clicked":self.close,
		"on_salir_activate":self.destroy,
		"on_volumen_value_changed":self.cb_master_slider_change,
		"on_AbrirB_clicked":self.abrir_archivos,
		"on_editar_clicked":self.edicion,
		"on_cancel_edit_clicked":self.stop_edicion,
		"on_ok_edit_clicked":self.save
		}
		"""eventHandlers"""
		
        	builder.connect_signals(dict)
		"""connect signals"""

	def abrir_archivos(self,widget):
		"""Add files to playlist"""
		pattern = (".mp3") 	
		self.filtro.set_name("*.mp3")
		for name, pattern in filepattern:
 			self.filtro.add_pattern(pattern)         	
		self.agregar_ventana.add_filter(self.filtro)
		respt=self.agregar_ventana.run()
		self.agregar_ventana.remove_filter(self.filtro)
		self.agregar_ventana.hide()
		dom = minidom.parse(path.TRACK)
		wml = dom.getElementsByTagName('wml')
		if respt == -5:
			fileselected = self.agregar_ventana.get_filenames()
			for files in fileselected:
				(dirs,files)= os.path.split(files)
				self.medialist.append([files,dirs])
				maincard = dom.createElement("pista")
				wml[0].appendChild(maincard)
				nm = dom.createElement("track")
				maincard.appendChild(nm)
				nombre = dom.createTextNode(files)
				nm.appendChild(nombre)
				dr = dom.createElement("ruta")
				maincard.appendChild(dr)
				paths = dom.createTextNode(dirs)
				dr.appendChild(paths)
			xmldocument = open(path.TRACK,"w")
			dom.writexml(xmldocument)
			xmldocument.close()

	def delete(self,widget):
		"""delete selected file from playlist"""
		select = self.tree.get_selection()
		filepath = path.on_tree_selection_changed(select)
		(modelo,filas) = select.get_selected_rows()
		for i in filas:
				for token in i:
					if token == '(' or token == ' ' or token == ',' or token == ')':
						pass
					else:
						node = token
				val = int(node)
				iterador = modelo.get_iter(i)
		treeiter = self.medialist.remove(iterador)
		dom = minidom.parse(path.TRACK)
		found = -1
		for i in range(0,len(dom.getElementsByTagName("track"))):
			if filepath.find(dom.getElementsByTagName("track")[i].firstChild.data) >= 0:
				found = i
		dom.getElementsByTagName("wml")[0].removeChild(dom.getElementsByTagName("pista")[found])
		xmldocument = open(path.TRACK,"w")
		dom.writexml(xmldocument)
		xmldocument.close()

	def clean(self,widget):
		"""clean playlist"""
		doc = open(path.TRACK,"w")
		doc.write('<?xml version="1.0" ?><wml></wml>')
		doc.close()
		self.medialist.clear()

	def edicion(self,widget):
		"""edit meta data"""
		try:
			select = self.tree.get_selection()
			filepath = path.on_tree_selection_changed(select)
			tag = eyeD3.Tag()
			tag.link(filepath)
			self.stock_album.set_text(tag.getAlbum())
			self.stock_interp.set_text(tag.getArtist())
			self.stock_titulo.set_text(tag.getTitle())
			self.window_edicion.show()
		except:
			pass

	def stop_edicion(self,widget):
		"""hide editor"""
		self.window_edicion.hide()

	def save(self,widget):
		"""save changes to meta data"""
		select = self.tree.get_selection()
		filepath = path.on_tree_selection_changed(select)
		tag = eyeD3.Tag()
		tag.link(filepath)
		tag.setAlbum(self.stock_album.get_text())
		tag.setArtist(self.stock_interp.get_text())
		tag.setTitle(self.stock_titulo.get_text())
		tag.update()
		self.window_edicion.hide()

	def cb_master_slider_change(self, widget,event,data=None):
		"""change master volume"""
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' +\
			str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass
 
	def about(self,widget):
		"""show about window"""
		self.help.show()
	
	def close(self,widget):
		"""hide about window"""
		self.help.hide()
	
	def destroy(self,widget):
		"""Close main program"""
		gtk.main_quit()
		self.hilo.stop()

	def play(self,widget):
		"""start playing"""
		self.gst_builder.play_state()
	
	def pause(self,widget):
		"""pause song"""
		self.player.set_state(gst.STATE_PAUSED)
		self.info.set_text(" Se ha pausado la reproduccion")
		self.state,self.dur = self.hilo.pause()	
		self.controler = 1
		
	def prev(self,widget):
		"""return to previous song"""
		self.gst_builder.prev_state()
		
	
	def next(self,widget):
		"""got to next song"""
		self.gst_builder.next_state()

	def stop(self,widget):
		"""stop playing, this may erase map playing"""
		self.gst_builder.stop_state()	

if __name__ == "__main__":
    main()
    gtk.main()


