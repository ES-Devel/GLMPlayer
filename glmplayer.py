#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  pg_hba.con
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

"""Programa principal - main program
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing - de pruebas
:license: GPL"""
	
from gi.repository import Gtk,GdkPixbuf, GObject
from plugins import playbin
loop = GObject.MainLoop()	
import subprocess
import random
from core import window,importWindow,about,edit,mediaList,resources
import ConfigParser  

cfg = ConfigParser.ConfigParser() 
cfg.read(["config/glmplayer.cfg"])


class main:

	def __init__(self):
		
		self.Storage = resources.ConfigFiles()+"track.xml"
		self.img = resources.uiPath()+"artwork.png"
		self.Noimg = resources.uiPath()+"NOCD.png"
		
		try:
			self.__builder = Gtk.Builder()
			self.__builder.add_from_file(resources.ui())
		except:
			print "Se encontraron errores al cargar la interfaz grafica"
		 
		try: 
			self.__window = window.Glmplayer(
						self,
						self.__builder
					)
		except:
			print "No se puede construir la ventana principal"
		
		self.__objects = (
			"arbol_pistas",
			"media",
			"selec",
			"caratula",
			"info",
			"artista",
			"album",
			"titulo",
			"duracion",
			"volumen",
			"bar",
			"stock_interp",
			"stock_titulo",
			"stock_album",
			"herramientas",
			"random",
			"repeat"
			)	
		
		try:	
			self.child = self.__window.Start(
						"ventana_principal",
						self.__objects
					)
		except:
			print "Error al iniciar la ventana"
		
		
		self.__window.getInstance().maximize()
		
		try:  
			self.importFiles = importWindow.importWindow(
										self.__builder,
										self,
										self.Storage
									)
		except:
			print "Error al procesar la ventana para importar archivos"
		
		try:
			self.LoadSettings( )
		except:
			print "Error al cargar las preferencias"
		
		try:
			self.about = about.aboutWindow(
						self.__builder,
						self
					)
		except:
			print "Error al cargar ventana de informacion"
		
		try:
			self.edit = edit.editWindow(
						self.__builder,
						self,
						self.child["arbol_pistas"]
					)
		except:
			print "Error al cargar la ventana de edicion"
		
		try:
			self.LoadChildWindows( )
		except:
			print "Error al iniciar las ventanas hijas"
		
		try:
			self.gst_builder = playbin.Stream(
						self,
						self.child["caratula"],
						self.child["bar"],
						self.child["arbol_pistas"],
						self.img,
						self.Noimg,
						self.child["info"],
						self.child["artista"],
						self.child["album"],
						self.child["duracion"],
						self.child["titulo"]
					)
		except:
			print "Error al instanciar el controlador de reproduccion"
		
		try:	
			self.PlayList = mediaList.MediaList(
						self,
						self.child["media"],
						self.child["arbol_pistas"],
						self.Storage
					)
		except:
			print "Error al instanciar el arbol de almacenamiento"
		
		try:		
			self.PlayList.Search()
		except:
			print "Error al cargar las pistas"	
		
		self.TOTAL = self.NumSongs( )
		
		try:
			self.child["caratula"].set_from_pixbuf(
					GdkPixbuf.Pixbuf.new_from_file_at_size(
							resources.uiPath()+"NOCD.png",
							200,
							200
						)
					)
		except:
			print "No se puede cargar la imagen provisional"
		
		self.child["info"].push(
				self.child["info"].get_context_id("load done"),
				"Done, "+str(self.TOTAL)+" Songs"
			)
		
		dict = self.getSignals( )
		
		try:
			self.__window.getBuilder().connect_signals(dict)
		except:
			print "No se pueden cargar las señales"
		
	def cb_master_slider_change(self, widget,event,data=None):		
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' +\
			str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass
	
	def destroy(self,widget):
		Gtk.main_quit()
		self.gst_builder.KILL()

	def play(self,widget):
		self.gst_builder.play_state()
	
	def pause(self,widget):
		self.gst_builder.pause_state()
		
	def prev(self,widget):
		self.gst_builder.prev_state()
	
	def next(self,widget):
		self.gst_builder.next_state()

	def stop(self,widget):
		self.gst_builder.stop_state()	
	
	def random(self,widget):
		if self.child["random"].get_active() == False:
			cfg.set("playing seetings", "random",0)
			self.gst_builder.MAPA = range(0,self.TOTAL)
			select = self.child["arbol_pistas"].get_selection()
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
			self.gst_builder.current = val + 1
			 
		else:  
			cfg.set("playing seetings", "random",1)
			self.gst_builder.MAPA = range(0,self.TOTAL)
			random.shuffle(self.gst_builder.MAPA)
			self.gst_builder.current = 0
		f = open("config/glmplayer.cfg", "w")  
		cfg.write(f)  
		f.close()
		
	def repeat(self,widget):
		if self.child["repeat"].get_active() == False:
			cfg.set("playing seetings", "repeat",0)
		else:  
			cfg.set("playing seetings", "repeat",1)
		f = open("config/glmplayer.cfg", "w")  
		cfg.write(f)  
		f.close()
		
	def LoadChildWindows(self):
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")   
	
	def LoadSettings(self):
		if int(cfg.get("playing seetings","random")) == 0:
			self.child["random"].set_active(False)
		else:
			self.child["random"].set_active(True)
		if int(cfg.get("playing seetings","repeat")) == 0:
			self.child["repeat"].set_active(False)
		else:
			self.child["repeat"].set_active(True)
	
	def NumSongs(self):
		try:
			selections = self.child["arbol_pistas"].get_selection()
			(modelo,filas) = selections.get_selected_rows()
			iterador = modelo.get_iter(0)
			cont = 0
			while iterador != None:
				iterador = modelo.iter_next(iterador)
				cont = cont + 1
			return cont
		except:
			return 0
			
	def getSignals(self):
		return {"on_agregar_activate": self.importFiles.OpenDialog,
		"gtk_main_quit":self.destroy,
		"on_delete_clicked":self.PlayList.delete,
		"on_play_clicked":self.play,
		"on_random_toggled":self.random,
		"on_repeat_toggled":self.repeat,
		"on_pause_clicked":self.pause,
		"on_prev_clicked":self.prev,
		"on_next_clicked":self.next,
		"on_stop_clicked":self.stop,
		"on_ayud_activate":self.about.Show,
		"on_about_tool_clicked":self.about.Show,
		"on_clean_clicked":self.PlayList.clean,
		"on_close_about_clicked":self.about.Hide,
		"on_salir_activate":self.destroy,
		"on_volumen_value_changed":self.cb_master_slider_change,
		"on_AbrirB_clicked":self.importFiles.OpenDialog,
		"on_editar_clicked":self.edit.edicion,
		"on_cancel_edit_clicked":self.edit.stop_edicion,
		"on_ok_edit_clicked":self.edit.save
		}
					
if __name__ == "__main__":
    main()   
    loop.quit()
    Gtk.main()
