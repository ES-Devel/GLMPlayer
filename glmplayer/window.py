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

from glmplayer_lib import WindowBase, resources

from gi.repository import Gtk


class Glmplayer( WindowBase.window ):

	def __init__(self,parent,builder):
		WindowBase.window.__init__ ( self , parent , builder )
		
	def Start( self , name , objects ):
		self.instance( self.getBuilder( ).get_object( name ) )
		child = { }
		
		for item in objects:
			child[item] = self.getBuilder( ).get_object( item )
			
		context = child["herramientas"].get_style_context( )
		context.add_class( Gtk.STYLE_CLASS_PRIMARY_TOOLBAR )
		return child
		

