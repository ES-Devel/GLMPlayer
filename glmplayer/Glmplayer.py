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

from glmplayer_lib import playbin, resources, settings, glmplayerconfig, statusbarlib, metadatalib, threadlib

from gi.repository import Gtk,GdkPixbuf, GLib 

import subprocess 

import time

GLib.threads_init()
    
class main:

	def __init__(self):
		
		# env vars 
		self.isPaused = False
		self.len = 0
		self.prov = 0
		self.__numErrors__ = 0
		self.__errorLog__ = []
		self.storageFile = glmplayerconfig.get_data_path()+"/config/track.xml"
		self.ui_path = glmplayerconfig.get_data_path()+"/ui/glmplayer.glade"
		self.conf_path = glmplayerconfig.get_data_path()+"/config/glmplayer.cfg"
		self.noArtworkFile = glmplayerconfig.get_data_path()+"/ui/NOCD.png" 
		
		# config handler
		# see glmplayer_lib/settings.py for more details about how this class works
		self.configManager = settings.ConfigManager( self ) 
		self.configManager.setConfigFile( self.conf_path ) 
		
		# Gtk.Builder
		self.__builder = Gtk.Builder( )
		self.__builder.add_from_file( self.ui_path )
		
		# see glmplayer/window.py for more details about how this class works 
		self.__window = window.Glmplayer( self, self.__builder )
		# see glmplayer_lib/resources.py for more details about resources.objects
		self.child = self.__window.Start( "ventana_principal", resources.objects )
		self.__window.getInstance( ).maximize( )
		
		# see glmplayer/importWindow.py for more details about how this class works  
		self.importFiles = importWindow.importWindow( self.__builder, self, self.storageFile )
		
		# see glmplayer/about.py for more details about how this class works
		self.about = about.aboutWindow( self.__builder, self )	
		
		# see glmplayer/edit.py for more details about how this class works
		self.edit = edit.editWindow( self.__builder, self, self.child["arbol_pistas"] )
		
		self.child["tiempo"].set_text("00:00")
		
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
		self.gst_builder = playbin.Stream( self, self.child["caratula"], self.child["tiempo"], self.child["arbol_pistas"],
					self.metadatahandler )
					
		self.threadhandler = None
				
        # see glmplayer/mediaList.py for more details about how this class works
		self.PlayList = mediaList.MediaList( self, self.child["media"],self.child["arbol_pistas"], self.storageFile ) 
		
		# update MediaList		
		self.__numErrors__, self.__errorLog__ = self.PlayList.Search( )
		
		self.child["caratula"].set_from_pixbuf( GdkPixbuf.Pixbuf.new_from_file_at_size( self.noArtworkFile, 200, 200 ) )

		dict = resources.getSignals( self )
		self.__window.getBuilder( ).connect_signals(dict)
		self.finishInitProc( )
		
	def cb_master_slider_change(self, widget,event,data=None):		
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE )
			proc.wait()
		except:
			pass
	
	def destroy(self,widget):
	    if self.threadhandler != None:
	         self.threadhandler.stopthread()
		Gtk.main_quit( )	    
	
	def play(self):
		self.len, st = self.gst_builder.play_state( )
		self.statusBar.setText(st)
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		self.threadhandler = threadlib.threadhandler( self, self.len )
		self.threadhandler.start()
	
	def pause(self):
	    self.isPaused = True
		self.statusBar.setText( self.gst_builder.pause_state( ) )
		
	def prev(self,widget):
		self.len, st = self.gst_builder.prev_state( )
		self.statusBar.setText(st)
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
	
	def next(self,widget):
	    self.sig( )

    def next2(self,widget):
        # thread handler
        self.det()
        time.sleep(1)
	    self.sig( )
    
	def stop(self,widget):
	    self.det()   
	    self.child["play"].set_active(False)
	        
    def sig(self):
		self.len, st = self.gst_builder.next_state( )
		self.statusBar.setText(st)
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		self.threadhandler = threadlib.threadhandler( self, self.len )
		self.threadhandler.start()
	
	def det(self):
		self.statusBar.setText( self.gst_builder.stop_state( ) )
		if self.threadhandler != None:
	         self.threadhandler.stopthread()
	    self.threadhandler = None
		
	def verify(self,widget):
	    if self.child["play"].get_active() == True:
	        if self.isPaused:
	            pass
	        else:
	            self.det( )
	        self.play( )
	    else:
	        self.pause( )
	        
	def LoadChildWindows(self):
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")
	        
	def finishInitProc(self):
	    # last step at init process
	    self.statusBar.setText("Done") 
		self.child["ErrorLogButton"].set_label("Errores ("+str(self.__numErrors__)+")")    
    
