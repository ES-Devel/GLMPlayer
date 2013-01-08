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

"""Window Base
:author: william parras
:organization: EsDevel Team
:contact: william.parras.mendez@gmail.com
:version: 0.1
:status: testing
:license: GPL"""

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
