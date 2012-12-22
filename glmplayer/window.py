# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
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
		

