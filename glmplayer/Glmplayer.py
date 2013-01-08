# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE
	
from gi.repository import Gtk,GdkPixbuf, GLib #interfaz grafica

import subprocess # subprocesos - modificar volumen

from glmplayer_lib import resources, settings # ruta hacia configuraciones y ui

import window,importWindow,about,edit,mediaList # ventanas

from glmplayer_lib import playbin # plugins

import threading

import time

GLib.threads_init()
    
class main:

	def __init__(self):
		
		# define algunas constantes del entorno
		self.Storage = "track.xml" # xml playlist
		self.img = "artwork.png" # arte del album
		self.Noimg = "NOCD.png" # imagen en caso de no econtrar el arte
		self.isPaused = False
		# manejador de configuracion
		# posteriormente se indica la ruta del archivo
		# para mas detalles de como esta clase trabaja 
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer_lib/settings.py
		self.configManager = settings.ConfigManager( self ) 
		self.configManager.setConfigFile( "glmplayer.cfg" ) 
		
		# Gtk.Builder
		self.__builder = Gtk.Builder()
		try:
		    self.__builder.add_from_file("data/ui/glmplayer.glade")
		except:
		    self.__builder.add_from_file("usr/local/share/Glmplayer/ui/glmplayer.glade")
		  
		# inicializa la ventana principal
		# para mas detalles de como esta clase trabaja
		# ver el archivo $[PROJEC_ROOT_DIRECTORY]/glmplayer/Glmplayer.py 
		self.__window = window.Glmplayer( self, self.__builder )	
		self.child = self.__window.Start( "ventana_principal", resources.objects )
		self.child["tiempo"].set_text("00:00")
		
		self.initUpdate( )
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
				
		self.PlayList.Search( ) # realiza la busqueda de pistas	
		
		try:
		    self.child["caratula"].set_from_pixbuf(
			    	GdkPixbuf.Pixbuf.new_from_file_at_size(
			    			"data/ui/NOCD.png",
				    		200,
					    	200
				    	)
				    ) # inicializa el elemento que muestra el arte
		except:
		    self.child["caratula"].set_from_pixbuf(
			    	GdkPixbuf.Pixbuf.new_from_file_at_size(
			    			"/usr/local/share/Glmplayer/ui/NOCD.png",
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
	    self.flag = False
		Gtk.main_quit( )	    
	
	def pause(self):
	    self.flag = False
	    self.isPaused = True
		self.gst_builder.pause_state( )
		
	def prev(self,widget):
	    self.initUpdate( )
	    self.flag = True
		self.len = self.gst_builder.prev_state( )
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		self.hilo = threading.Thread(target=self.updateBar)
		self.hilo.start()
	
	def next(self,widget):
	    self.sig( )


	def stop(self,widget):
	    self.detener()
		
	def LoadChildWindows(self):
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")   
		
    def updateBar( self ):
        while (self.current < self.len ) and self.flag == True:
			step = 96 / self.len
			nxt = self.current * step
			self.child["bar"].set_value(nxt)
			self.child["tiempo"].set_text(self.timeFormat(self.secondToMin(self.curr2)))
			time.sleep(1)
			self.current = self.current + 1
			self.curr2 = self.curr2 + 1
		if not( self.current < self.len ) and ( self.current != 0 or self.len != 0 ):
		    self.child["handler"].clicked( )
		print "final"
	
	def initUpdate( self ):
	    self.flag = False
		self.len = 0
		self.current = 0
		self.prov = 0
		self.child["bar"].set_value(0)
		self.child["tiempo"].set_text("00:00")
		self.minCt = 0
		self.curr2 = 0
		
		
	def secondToMin(self, sec):
	    if sec < 60 :
	        return sec
	    else:
	        self.curr2 = 0
	        self.minCt = self.minCt + 1  
	        return sec % 60
	        
	def timeFormat(self, time):
	    if time < 10:
	        return "0"+str(self.minCt)+":0"+str(time)
	    else:
	        return "0"+str(self.minCt)+":"+str(time)
	        
    def sig(self):
        self.initUpdate( )
	    self.flag = True
		self.len = self.gst_builder.next_state( )
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		hilo = threading.Thread(target=self.updateBar)
		hilo.start()
	
	def detener(self):
	    self.initUpdate( )
		self.gst_builder.stop_state( )
		
	def reproducir(self):
		self.len = self.gst_builder.play_state( )
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		self.flag = True
		hilo = threading.Thread(target=self.updateBar)
		hilo.start()
		
	def verify(self,widget):
	    if self.child["play"].get_active() == True:
	        if self.isPaused:
	            pass
	        else:
	            self.detener()
	        self.reproducir()
	    else:
	        self.pause()
    
