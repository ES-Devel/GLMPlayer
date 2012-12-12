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
#  

"""Main program
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

try:
	from gi.repository import Gtk, GObject,GdkPixbuf
	loop = GObject.MainLoop()
except:
	print "Problemas de dependencias: gtk3"
	
import subprocess
import random
from plugins import playbin
from core import window,importWindow,about,edit,mediaList,resources
import ConfigParser  

cfg = ConfigParser.ConfigParser()
"""variable global: manejador de archivo de configuracion""" 
cfg.read(["config/glmplayer.cfg"])  


class main:
	"""clase principal: Inicia la ejecucion del programa"""

	def __init__(self):
		"""inicializacion de variables
		:return: None"""
		self.Storage = "track.xml"
		"""Archivo de almacenamiento de pistas"""
		self.img = resources.uiPath()+"artwork.png"
		"""ruta hacia la caratula de album"""
		self.Noimg = resources.uiPath()+"NOCD.png"
		"""ruta hacia la caratula vacia"""
		self.__builder = Gtk.Builder()
		"""gtk Builder, Constructor de interfaz grafica"""
		self.__builder.add_from_file(resources.ui())
		"""Carga el XML que define la interfaz""" 
		self.__window = window.Glmplayer(self,self.__builder)
		"""Almacena la instancia de la ventana principal"""  
		self.__objects = ("arbol_pistas","media","selec","caratula",\
		"info","artista","album","titulo","duracion","volumen","bar",\
		"stock_interp","stock_titulo","stock_album","herramientas",\
		"random","repeat")
		"""Especifica los nombres de los objetos en el programa, estos
		nombres se encuentran en el XML de la interfaz grafica"""	
		self.child = self.__window.Start("ventana_principal",self.__objects)
		"""Llama al metodo de inicio de la ventana, recibe los objetos
		como parametro y los crea dentro del programa. Almacena los valores
		en un dicionario para acceder a ellos por nombre"""
		self.importFiles = importWindow.importWindow(self.__builder,\
		self,resources.ConfigFiles()+self.Storage)
		"""Crea la instancia de la ventana para importar archivos"""
		################################################################
		# Revisa el archivo de configuracion y verifica que estado
		# tenian los botones cuando se cerro el programa
		if int(cfg.get("playing seetings","random")) == 0:
			self.child["random"].set_active(False)
		else:
			self.child["random"].set_active(True)
		if int(cfg.get("playing seetings","repeat")) == 0:
			self.child["repeat"].set_active(False)
		else:
			self.child["repeat"].set_active(True)
		################################################################
		self.about = about.aboutWindow(self.__builder,self)
		"""crea la instancia de ventana de About - Acerca de"""
		self.edit = edit.editWindow(self.__builder,self,self.child["arbol_pistas"])
		"""crea la instancia de la ventana de edicion de metadata"""
		################################################################
		# Asigna nombres a las ventanas, son los nombres en el XML de
		# la interface grafica
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")
		################################################################
		self.gst_builder = playbin.Stream(self,self.child["caratula"],self.child["bar"],\
		self.child["arbol_pistas"],self.img,self.Noimg,self.child["info"],self.child["artista"],\
		self.child["album"],self.child["duracion"],self.child["titulo"])
		"""crea el controladore de la reproduccion"""	
		self.PlayList = mediaList.MediaList(self,self.child["media"],\
		self.child["arbol_pistas"],resources.ConfigFiles()+self.Storage)
		"""crea el objeto de almacenamiento de datos"""
		self.PlayList.Search()	
		"""llama al metodo de busqueda de pistas en el arbol de almacenamiento
		asociado"""
		################################################################
		# Obtiene el numero de canciones en el arbol de almacenamiento
		selections = self.child["arbol_pistas"].get_selection()
		(modelo,filas) = selections.get_selected_rows()
		iterador = modelo.get_iter(0)
		cont = 0
		while iterador != None:
			iterador = modelo.iter_next(iterador)
			cont = cont + 1
		self.TOTAL = cont
		################################################################
		self.child["caratula"].set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_size(\
		resources.uiPath()+"NOCD.png", 200, 200))
		"""asigna la caratula vacia"""
		self.child["info"].push(self.child["info"].get_context_id("load done"),\
		"Done, "+str(self.TOTAL)+" Songs")
		"""Indica el estado en la barra de estado"""
		dict = {"on_agregar_activate": self.importFiles.OpenDialog,
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
		self.__window.getBuilder().connect_signals(dict)
		"""Conecta todas las 'signals' indicadas en el diccionario"""
		
	def cb_master_slider_change(self, widget,event,data=None):
		"""Controla el control de volumen con un subproceso"""		
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' +\
			str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass
	
	def destroy(self,widget):
		"""Destruye la ventana y detiene el hilo de reproduccion"""
		Gtk.main_quit()
		self.gst_builder.KILL()

	def play(self,widget):
		"""Llama al metodo de reproduccion"""
		self.gst_builder.play_state()
	
	def pause(self,widget):
		"""Llama al metodo para pausar la reproduccion"""
		self.gst_builder.pause_state()
		
	def prev(self,widget):
		"""Llama al metodo para buscar la pista anterior"""
		self.gst_builder.prev_state()
	
	def next(self,widget):
		"""Llama al metodo para ir a la siguiente pista"""
		self.gst_builder.next_state()

	def stop(self,widget):
		"""Detiene la reproduccion"""
		self.gst_builder.stop_state()	
	
	def random(self,widget):
		"""Evento random, modifica el Mapa de reproccion"""
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
		"""evento repetir, indica si se repite la lista"""
		if self.child["repeat"].get_active() == False:
			cfg.set("playing seetings", "repeat",0)
		else:  
			cfg.set("playing seetings", "repeat",1)
		f = open("config/glmplayer.cfg", "w")  
		cfg.write(f)  
		f.close()   

if __name__ == "__main__":
    main()
    loop.quit()   
    Gtk.main()


