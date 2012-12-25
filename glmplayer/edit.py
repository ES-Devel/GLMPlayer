# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from glmplayer_lib import WindowBase, resources

try:
	import eyeD3
except ImportError:
	print "To run this program correctly you must install python-eyed3"

class editWindow( WindowBase.window ):

	def __init__( self,builder,parent,MediaTree ):
		WindowBase.window.__init__( self , parent , builder )
		self.Tree = MediaTree
	
	def edicion(self,widget):
		try:
			select = self.Tree.get_selection(  )
			filepath = resources.on_tree_selection_changed( select )
			tag = eyeD3.Tag( )
			tag.link( filepath )
			
			self.getParent(	).child["stock_album"].set_text(	tag.getAlbum(	))
			self.getParent(	).child["stock_interp"].set_text(	tag.getArtist(	))
			self.getParent(	).child["stock_titulo"].set_text(	tag.getTitle(	))
			self.Show_(	)
		except:
			print "Ocurrio un error mientras se editaban las pistas"

	def stop_edicion(self,widget):
		self.Hide_()

	def save(self,widget):
		select = self.Tree.get_selection(	)
		filepath = resources.on_tree_selection_changed(	select	)
		tag = eyeD3.Tag(	)
		tag.link( filepath )
		
		tag.setAlbum(	self.getParent(	).child["stock_album"].get_text(	))
		tag.setArtist(	self.getParent(	).child["stock_interp"].get_text(	))
		tag.setTitle(	self.getParent(	).child["stock_titulo"].get_text(	))
		tag.update(	)
		self.Hide_(	)
