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
#  
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

import gtk
import subprocess
from plugins import playbin
from core import window,importWindow,about,edit,mediaList,resources

class main:
	"""main class: runs program"""

	def __init__(self):
		"""start runing all windows
		:return: None"""
		self.Storage = "track.xml"
		self.img = resources.uiPath()+"artwork.png"
		self.Noimg = resources.uiPath()+"NOCD.png"
		# main window
		self.__builder = gtk.Builder()
		self.__builder.add_from_file(resources.ui()) 
		self.__window = window.Glmplayer(self,self.__builder)  
		self.__objects = ("arbol_pistas","media","selec","caratula",\
		"info","artista","album","titulo","duracion","volumen","bar",
		"stock_interp","stock_titulo","stock_album")
		self.__window.Start("ventana_principal",self.__objects)
		# import, about, edit windows
		self.importFiles = importWindow.importWindow(self.__builder,\
		self,resources.ConfigFiles()+self.Storage)
		self.about = about.aboutWindow(self.__builder,self)
		self.edit = edit.editWindow(self.__builder,self,self.child["arbol_pistas"])
		# set windows by Name
		self.importFiles.Start("Add")
		self.about.Start("About")
		self.edit.Start("edit")
		# gstreamer builder object
		self.gst_builder = playbin.Stream(self,self.child["caratula"],self.child["bar"],\
		self.child["arbol_pistas"],self.img,self.Noimg,self.child["info"],self.child["artista"],\
		self.child["album"],self.child["duracion"],self.child["titulo"])	
		# creates mediaList to store media data
		self.PlayList = mediaList.MediaList(self,self.child["media"],\
		self.child["arbol_pistas"],resources.ConfigFiles()+self.Storage)
		# search for songs
		self.PlayList.Search()	
		
		
		self.child["caratula"].set_from_file(resources.uiPath()+"NOCD.png")
		
		self.child["info"].push(self.child["info"].get_context_id("load done"),"Done")
		
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

if __name__ == "__main__":
    main()
    gtk.main()


