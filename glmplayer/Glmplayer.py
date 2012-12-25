# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
	
from gi.repository import Gtk,GdkPixbuf #interfaz grafica

import subprocess # subprocesos - modificar volumen

from glmplayer_lib import resources, settings # ruta hacia configuraciones y ui

import window,importWindow,about,edit,mediaList # ventanas

from glmplayer_lib.plugins import playbin # plugins

    
class main:

	def __init__(self):
		
		# define algunas constantes del entorno
		# para mas detalles sobre estas definiciones
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer_lib/resources.py
		self.Storage = resources.ConfigFiles()+"track.xml" # xml playlist
		self.img = resources.uiPath()+"artwork.png" # arte del album
		self.Noimg = resources.uiPath()+"NOCD.png" # imagen en caso de no econtrar el arte
		# manejador de configuracion
		# posteriormente se indica la ruta del archivo
		# para mas detalles de como esta clase trabaja 
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer_lib/settings.py
		self.configManager = settings.ConfigManager( self ) 
		self.configManager.setConfigFile( "data/config/glmplayer.cfg" ) 
		
		# Gtk.Builder
		self.__builder = Gtk.Builder()
		self.__builder.add_from_file(resources.ui())
		  
		# inicializa la ventana principal
		# para mas detalles de como esta clase trabaja
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer/Glmplayer.py 
		self.__window = window.Glmplayer( self, self.__builder )	
		self.child = self.__window.Start( "ventana_principal", resources.objects )
		
		self.__window.getInstance( ).maximize( ) # maximiza la ventana
		
		# crea una instancia para la ventana agregar archivos
		# para mas detalles de como esta clase trabaja
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer/importWindow.py  
		self.importFiles = importWindow.importWindow( self.__builder, self, self.Storage )
		# crea una instancia para la ventana acerca de
		# para mas detalles de como esta clase trabaja
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer/about.py
		self.about = about.aboutWindow( self.__builder, self )
		
		self.configManager.LoadSettings( )
		
		self.edit = edit.editWindow( self.__builder, self, self.child["arbol_pistas"] )
		
		self.LoadChildWindows( ) # carga los hijos en la ventana
		
		# inicia control de reproduccion con todos sus
		# Elementos asociados
		# para mas detalles de como esta clase trabaja
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer_lib/plugins/playbin.py
		self.gst_builder = playbin.Stream(
					self,
					self.child["caratula"],
					self.child["tiempo"],
					self.child["arbol_pistas"],
					self.img,
					self.Noimg,
					self.child["info"],
					self.child["artista"],
					self.child["album"],
					self.child["duracion"],
					self.child["titulo"]
				)
				
        # para mas detalles de como esta clase trabaja
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer/mediaList.py
		self.PlayList = mediaList.MediaList(
					self,
					self.child["media"],
					self.child["arbol_pistas"],
					self.Storage
				) # inicia el controlador del playlist
		try:
		    self.PlayList.Search( ) # realiza la busqueda de pistas
		except:
		    pass	
		
		
		self.child["caratula"].set_from_pixbuf(
				GdkPixbuf.Pixbuf.new_from_file_at_size(
						resources.uiPath()+"NOCD.png",
						200,
						200
					)
				) # inicializa el elemento que muestra el arte
		
		self.child["info"].push(
				self.child["info"].get_context_id("load done"),
				"Done "
			) # muestra el estado del programa
		
		dict = resources.getSignals( self ) # define los eventos
		
		self.__window.getBuilder( ).connect_signals(dict) # conecta los eventos
		
	def cb_master_slider_change(self, widget,event,data=None):		
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' +\
			str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass
	
	def destroy(self,widget):
		Gtk.main_quit( )

	def play(self,widget):
		self.gst_builder.play_state( )
	
	def pause(self,widget):
		self.gst_builder.pause_state( )
		
	def prev(self,widget):
		self.gst_builder.prev_state( )
	
	def next(self,widget):
		self.gst_builder.next_state( )


	def stop(self,widget):
		self.gst_builder.stop_state( )
		
	def LoadChildWindows(self):
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")   
	
