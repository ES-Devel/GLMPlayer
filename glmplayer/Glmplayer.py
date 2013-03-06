# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
from glmplayer import window,importWindow,about,edit,mediaList 

from glmplayer_lib import playbin, resources, settings, glmplayerconfig, statusbarlib, metadatalib, threadlib

from gi.repository import Gtk,GdkPixbuf, GLib 

import subprocess 

import time

GLib.threads_init()
    
class main:

	def __init__(self):
	
		'-------------- environment vars --------------'
		'check if playing' 
		self.isPaused = False
		'store file lenght - current playing'
		self.len = 0
		'aux file lenght storage'
		self.prov = 0
		'path to xml database'
		self.storageFile = glmplayerconfig.get_data_path()+"/config/track.xml"
		'path to ui'
		self.ui_path = glmplayerconfig.get_data_path()+"/ui/glmplayer.glade"
		'path to config file'
		self.conf_path = glmplayerconfig.get_data_path()+"/config/glmplayer.cfg"
		'path to artwork'
		self.noArtworkFile = glmplayerconfig.get_data_path()+"/ui/NOCD.png" 
		'----------------------------------------------'
		'config handler - this class manages configuration settings'
		# see glmplayer_lib/settings.py for more details about how this class works
		self.configManager = settings.ConfigManager( self ) 
		self.configManager.setConfigFile( self.conf_path ) 
		'Gtk.Builder - see Gtk or pygtk documentation to know about Gtk.Builder'
		self.__builder = Gtk.Builder( )
		self.__builder.add_from_file( self.ui_path )
		# see glmplayer/window.py for more details about how this class works 
		'self.child stores Gtk.Widgets'
		'resources.objects is a list with the Gtk.Widgets names'
		self.__window = window.Glmplayer( self, self.__builder )
		self.child = self.__window.Start( "ventana_principal", resources.objects )
		self.__window.getInstance( ).maximize( )
		# see glmplayer/importWindow.py for more details about how this class works
		'this class manages media import methods - needs xml file'  
		self.importFiles = importWindow.importWindow( self.__builder, self, self.storageFile )
		# see glmplayer/about.py for more details about how this class works
		'this class wraps about dialog content and methods'
		self.about = about.aboutWindow( self.__builder, self )	
		'load last settings'
		self.configManager.LoadSettings( )
		'load objects instances'
		self.LoadChildWindows( )
		'Gtk.StatusBar handler'
		# see glmplayer_lib/statusbarlib.py for more details about how this class works
		'manages Gtk.Statusbar - needs Gtk.StatusBar object'
		self.statusBar = statusbarlib.barhandler( self.child["info"] )
		'metadata handler'
		# see glmplayer_lib/metadatalib.py for more details about how this class works
		self.metadatahandler = metadatalib.metadataMp3(self.child,"artista","album","duracion","titulo")
		'playback handler'
		# see glmplayer_lib/playbin.py for more details about how this class works
		self.gst_builder = playbin.Stream( 
		            self, 
		            self.child["caratula"], 
		            self.child["tiempo"], 
		            self.child["arbol_pistas"],
					self.metadatahandler )
		'playback thread'			
		self.threadhandler = None
		'iterates over playlist'		
        # see glmplayer/mediaList.py for more details about how this class works
		self.PlayList = mediaList.MediaList( self, self.child["media"],self.child["arbol_pistas"], self.storageFile ) 
		'load data from xml - count errors on load (example: missing files)'		
		self.PlayList.Search( )
		# see glmplayer/edit.py for more details about how this class works
		'this class manages metadata edition - needs a Gtk.Treewiev'
		self.edit = edit.editWindow(self.__builder,self,self.child["arbol_pistas"],self.PlayList)
		self.edit.Start("edit")
        'create dictionaty with Gtk events'
		dict = resources.getSignals( self )
		'connect events with main Window'
		self.__window.getBuilder( ).connect_signals(dict)
		'update some gui stuff'
		self.finishInitProc( )
		
	def cb_master_slider_change(self, widget,event,data=None):
	    'uses subprocess to change volume'		
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE )
			proc.wait()
		except:
			pass
	
	def destroy(self,widget):
	    'first kills threads then stop gtk main thread'
	    if self.threadhandler != None:
	         self.threadhandler.stopthread()
	    'this will destroy gui'
		Gtk.main_quit( )	    
	
	def play(self):
	    'this will play a song but it will save file lenght and playing status'
		self.len, st = self.gst_builder.play_state( )
		self.statusBar.setText(st)
		'in case of paused song self.len could be none, so we must avoid it using aux var'
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		'starting threads'
		self.threadhandler = threadlib.threadhandler( self, self.len )
		self.threadhandler.start()
	
	def pause(self):
	    'pause current song'
	    self.isPaused = True
		self.statusBar.setText( self.gst_builder.pause_state( ) )
		
	def prev(self,widget):
	    'goes backward'
	    # first stop current song if playing
	    self.det()
		self.len, st = self.gst_builder.prev_state( )
		self.statusBar.setText(st)
		if self.len == None:
		    self.len = self.prov
		else:
		    self.prov = self.len
		self.threadhandler = threadlib.threadhandler( self, self.len )
		self.threadhandler.start()
	
	def next(self,widget):
	    'goes forward'
	    self.det()
	    self.sig( )

    def next2(self,widget):
        'this method is called when song goes forward automatically'
        # thread handler
        self.det()
        'this avoid threads lock'
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
	    'check if playing'
	    if self.child["play"].get_active() == True:
	        if self.isPaused:
	            pass
	        else:
	            self.det( )
	        self.play( )
	    else:
	        self.pause( )
	        
	def LoadChildWindows(self):
	    'load secondary windows'
		self.importFiles.Start("Add")
		self.about.Start("About")
	        
	def finishInitProc(self):
	    'last step at init process'
	    self.child["caratula"].set_from_pixbuf( GdkPixbuf.Pixbuf.new_from_file_at_size( self.noArtworkFile, 50, 50 ) )
	    self.child["tiempo"].set_text("00:00")
	    self.statusBar.setText("Done")    
		
	def active_row(self,p1,p2,p3):
	    'this will play a song using on-key-press event'
	    self.play()        
