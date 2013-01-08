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

def ui( ):
	return "/usr/local/share/Glmplayer/ui/glmplayer.glade"

def uiPath():
	return "/usr/local/share/Glmplayer/ui"

def ConfigFiles():
	return "/usr/local/share/Glmplayer/config/"

def reverse(list):
	if len(list)==1:
		return list
	else:
		return list[-1]+reverse(list[:-1])  

def on_tree_selection_changed(selection):
	model, treeiter = selection.get_selected()
	if treeiter != None:
		palabra = "" 
		contador = 0
		for letra in model[treeiter][5]:
			if letra != "\n":
				if letra == " " and contador == 0:
					pass
				else:	
					palabra = palabra+letra
					contador = contador+1
		contador = 0
		palabra = reverse(palabra)
		nueva = ""
		for letra in palabra:
			if letra != "\n":
				if letra == " " and contador == 0:
					pass
				else:	
					nueva = nueva+letra
					contador = contador+1
		palabra = reverse(nueva)+"/"
		contador = 0			
		for letra in model[treeiter][4]:
			if letra != "\n":
				if letra == " " and contador == 0:
						pass
				else:	
					palabra = palabra+letra
					contador = contador+1
		contador = 0
		palabra = reverse(palabra)
		nueva = ""
		for letra in palabra:
			if letra != "\n":
				if letra == " " and contador == 0:
					pass
				else:	
					nueva = nueva+letra
					contador = contador+1			 
		palabra = reverse(nueva)
		return palabra 	

def clearing(array):
	palabra = ""
	contador = 0
	for letra in array:
			if letra != "\n":
				if letra == " " and contador == 0:
						pass
				else:	
					palabra = palabra+letra
					contador = contador+1
	contador = 0
	palabra = reverse(palabra)
	nueva = ""
	for letra in palabra:
		if letra != "\n":
			if letra == " " and contador == 0:
				pass
			else:	
				nueva = nueva+letra
				contador = contador+1			 
	palabra = reverse(nueva)
	return palabra 

def cleanNode(i):
	for token in i:
		if token == '(' or token == ' ' or token == ',' or token == ')':
			pass
		else:
			return token
	
def getSignals( pointer ):
		return {"on_agregar_activate": pointer.importFiles.OpenDialog,
		"gtk_main_quit":pointer.destroy,
		"on_delete_clicked":pointer.PlayList.delete,
		"on_play_toggled":pointer.verify,
		"on_random_toggled":pointer.configManager.random,
		"on_repeat_toggled":pointer.configManager.repeat,
		"on_prev_clicked":pointer.prev,
		"on_next_clicked":pointer.next,
		"on_handler_clicked":pointer.next,
		"on_stop_clicked":pointer.stop,
		"on_ayud_activate":pointer.about.Show,
		"on_about_tool_clicked":pointer.about.Show,
		"on_clean_clicked":pointer.PlayList.clean,
		"on_close_about_clicked":pointer.about.Hide,
		"on_salir_activate":pointer.destroy,
		"on_volumen_value_changed":pointer.cb_master_slider_change,
		"on_AbrirB_clicked":pointer.importFiles.OpenDialog,
		"on_editar_clicked":pointer.edit.edicion,
		"on_cancel_edit_clicked":pointer.edit.stop_edicion,
		"on_ok_edit_clicked":pointer.edit.save
		}
		
objects = (
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
			"repeat",
			"tiempo",
			"play",
			"next",
			"handler",
			"icon"
			)
