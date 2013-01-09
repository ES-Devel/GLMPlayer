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
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from glmplayer import window,importWindow,about,edit,mediaList 

from glmplayer_lib import playbin, resources, settings, glmplayerconfig, statusbarlib, metadatalib

from gi.repository import Gtk,GdkPixbuf, GLib 

import subprocess 

import threading

import time


GLib.threads_init()
    
class main:

	def __init__(self):
		
		# env vars 
		self.isPaused = False
		self.__numErrors__ = 0
		self.__errorLog__ = []
		
		# config handler
		# see glmplayer_lib/settings.py for more details about how this class works
		self.configManager = settings.ConfigManager( self ) 
		self.configManager.setConfigFile( glmplayerconfig.get_data_path()+"/config/glmplayer.cfg" ) 
		
		# Gtk.Builder
		self.__builder = Gtk.Builder( )
		self.__builder.add_from_file( glmplayerconfig.get_data_path()+"/ui/glmplayer.glade" )
		
		# see glmplayer/window.py for more details about how this class works 
		self.__window = window.Glmplayer( self, self.__builder )
		# see glmplayer_lib/resources.py for more details about resources.objects
		self.child = self.__window.Start( "ventana_principal", resources.objects )
		self.__window.getInstance( ).maximize( )
		
		# see glmplayer/importWindow.py for more details about how this class works  
		self.importFiles = importWindow.importWindow( self.__builder, self, glmplayerconfig.get_data_path()+"/config/track.xml" )
		
		# see glmplayer/about.py for more details about how this class works
		self.about = about.aboutWindow( self.__builder, self )	
		
		# see glmplayer/edit.py for more details about how this class works
		self.edit = edit.editWindow( self.__builder, self, self.child["arbol_pistas"] )
		
		self.child["tiempo"].set_text("00:00")
		
		self.initUpdate( )
		
	    self.configManager.LoadSettings( )
		
		self.LoadChildWindows( )
		
		# Gtk.StatusBar handler
		# see glmplayer_lib/statusbarlib.py for more details about how this class works
		self.statusBar = statusbarlib.barhandler( self.child["info"] )
		
		# metadata handler
		# see glmplayer_lib/metadatalib.py for more details about how this class works
		self.metadatahandler = metadatalib.metadataMp3(self.child,"artista","album","duracion","titulo")
		
		# playbin handler
		# see glmplayer_lib/playbin.py for more details about how this class works
		self.gst_builder = playbin.Stream( self,
					self.child["caratula"],
					self.child["tiempo"],
					self.child["arbol_pistas"],
					self.metadatahandler
				)
				
        # see glmplayer/mediaList.py for more details about how this class works
		self.PlayList = mediaList.MediaList(
					self,
					self.child["media"],
					self.child["arbol_pistas"],
					glmplayerconfig.get_data_path()+"/config/track.xml"
				) 
		
		# update MediaList		
		self.__numErrors__, self.__errorLog__ = self.PlayList.Search( )
		
		self.child["caratula"].set_from_pixbuf(
			    GdkPixbuf.Pixbuf.new_from_file_at_size(
			    		glmplayerconfig.get_data_path()+"/ui/NOCD.png",
				    	200,
					    200
				    )
				 )

		
		dict = resources.getSignals( self )
		self.__window.getBuilder( ).connect_signals(dict)
		self.finishInitProc( )
		
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
		self.statusBar.setText( self.gst_builder.pause_state( ) )
		
	def prev(self,widget):
	    self.initUpdate( )
	    self.flag = True
		self.len, st = self.gst_builder.prev_state( )
		self.statusBar.setText(st)
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		self.hilo = threading.Thread(target=self.updateBar)
		self.hilo.start()
	
	def next(self,widget):
	    self.initUpdate( )
	    self.sig( )

    def next2(self,widget):
        self.initUpdate( )
        time.sleep(0.5)
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
	    self.flag = True
		self.len, st = self.gst_builder.next_state( )
		self.statusBar.setText(st)
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		hilo = threading.Thread(target=self.updateBar)
		hilo.start()
	
	def detener(self):
	    self.initUpdate( )
		self.statusBar.setText( self.gst_builder.stop_state( ) )
		
	def reproducir(self):
		self.len, st = self.gst_builder.play_state( )
		self.statusBar.setText(st)
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
	        
	def finishInitProc(self):
	    self.statusBar.setText("Done") 
		self.child["ErrorLogButton"].set_label("Errores ("+str(self.__numErrors__)+")")    
    
