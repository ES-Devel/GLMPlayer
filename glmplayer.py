#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main program
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

import gtk
import gst
import subprocess
from plugins import playbin
from core import window,importWindow,about,edit,mediaList,resources

class main:
	"""main class: runs program"""

	def __init__(self):
		"""start runing all windows
		:return: None"""
		# main window
		self.__window = window.Glmplayer(self,None)  
		self.__window.Set( )   		
		self.__window.Start("ventana_principal")
		# import, about, edit windows
		self.importFiles = importWindow.importWindow(self.__window.getBuilder(),self)
        	self.about = about.aboutWindow(self.__window.getBuilder(),self)
       		self.edit = edit.editWindow(self.__window.getBuilder(),self)
		# set windows by Name
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")
		# gstreamer builder object
		self.gst_builder = playbin.Stream(self)
		# info Label: shows current status		
        	self.info.set_text("No se ha reproducido nada aun")
		# creates mediaList to store media data
		self.PlayList = mediaList.MediaList(self)
		# search for songs
		self.PlayList.Search()	
		
        	self.time_song = 0
        	self.imagen.set_from_file(resources.uiPath()+"NOCD.png")
        	self.MAPA = [] 
        	self.current = 0
        	self.controler = 0
        	self.max = 0
		
        	dict = {"on_agregar_activate": self.importFiles.OpenDialog,
		"gtk_main_quit":self.destroy,
		"on_delete_clicked":self.PlayList.delete,
		"on_play_clicked":self.play,
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

	def cb_master_slider_change(self, widget,event,data=None):
		try:
			val = widget.get_value()
			proc = subprocess.Popen('/usr/bin/amixer sset Master ' +\
			str(val) + '%', shell=True, stdout=subprocess.PIPE)
			proc.wait()
		except:
			pass
	
	def destroy(self,widget):
		gtk.main_quit()
		self.hilo.stop()

	def play(self,widget):
		self.gst_builder.play_state()
	
	def pause(self,widget):
		self.player.set_state(gst.STATE_PAUSED)
		self.info.set_text(" Se ha pausado la reproduccion")
		self.state,self.dur = self.hilo.pause()	
		self.controler = 1
		
	def prev(self,widget):
		self.gst_builder.prev_state()
		
	
	def next(self,widget):
		self.gst_builder.next_state()

	def stop(self,widget):
		self.gst_builder.stop_state()	

if __name__ == "__main__":
    main()
    gtk.main()


