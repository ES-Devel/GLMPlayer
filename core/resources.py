#!/usr/bin/env python
# -*- coding: utf-8 -*-

def ui( ):
	"""path to ui
	:return: str"""
	return "ui/glmplayer.glade"

def uiPath():
	return "ui/"

def ConfigFiles():
	return "config/"

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
		for letra in model[treeiter][1]:
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
		for letra in model[treeiter][0]:
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
