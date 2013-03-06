# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-

from gi.repository import Gtk

import resources

class window( ):

	def __init__(self,parent,builder):
		self.__parent = parent
		self.__instance = None
		self.__builder = builder
		self.__name = " "

	def Start(self,name):
		self.instance ( self.getBuilder( ).get_object ( name ) )
		self.setName  ( name )

	def Show(self,widget):
		self.getInstance( ).show ( )

	def Show_(self):
		self.getInstance( ).show( )
	
	def Hide(self,widget):
		self.getInstance( ).hide( )

	def Hide_(self):
		self.getInstance( ).hide( )
	
	def instance(self,instance):
		self.__instance = instance
	
	def setName(self,name):
		self.__name = name
	
	def getName(self):
		return self.__name
		
	def getBuilder(self):
		return self.__builder

	def getParent(self):
		return self.__parent

	def getInstance(self):
		return self.__instance
